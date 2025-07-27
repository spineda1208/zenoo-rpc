"""
Base model classes for OdooFlow.

This module provides the foundation for type-safe Odoo record handling
using Pydantic models with ORM-like capabilities.
"""

from typing import Any, Dict, List, Optional, Type, TypeVar, Union, ClassVar
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator
from pydantic.fields import FieldInfo

from .relationships import LazyRelationship, RelationshipManager
from .fields import (
    RelationshipDescriptor,
    Many2OneDescriptor,
    One2ManyDescriptor,
    Many2ManyDescriptor,
)

T = TypeVar("T", bound="OdooModel")


class OdooModelMeta(type(BaseModel)):
    """Metaclass for OdooModel that sets up relationship descriptors."""

    def __new__(cls, name, bases, namespace, **kwargs):
        # Create the class first
        new_class = super().__new__(cls, name, bases, namespace, **kwargs)

        # Skip setup for base OdooModel class
        if name == "OdooModel":
            return new_class

        # Setup relationship descriptors
        cls._setup_relationship_descriptors(new_class)

        return new_class

    @staticmethod
    def _setup_relationship_descriptors(model_class):
        """Setup relationship descriptors for the model class."""
        if not hasattr(model_class, "model_fields"):
            return

        for field_name, field_info in model_class.model_fields.items():
            # Skip if descriptor already exists
            if hasattr(model_class, field_name) and isinstance(
                getattr(model_class, field_name), RelationshipDescriptor
            ):
                continue

            if (
                hasattr(field_info, "json_schema_extra")
                and field_info.json_schema_extra
            ):
                odoo_type = field_info.json_schema_extra.get("odoo_type")

                if odoo_type == "many2one":
                    comodel_name = field_info.json_schema_extra.get("odoo_relation")
                    if comodel_name:
                        descriptor = Many2OneDescriptor(
                            field_name, comodel_name, field_info
                        )
                        setattr(model_class, field_name, descriptor)

                elif odoo_type == "one2many":
                    comodel_name = field_info.json_schema_extra.get("odoo_relation")
                    if comodel_name:
                        descriptor = One2ManyDescriptor(
                            field_name, comodel_name, field_info
                        )
                        setattr(model_class, field_name, descriptor)

                elif odoo_type == "many2many":
                    comodel_name = field_info.json_schema_extra.get("odoo_relation")
                    if comodel_name:
                        descriptor = Many2ManyDescriptor(
                            field_name, comodel_name, field_info
                        )
                        setattr(model_class, field_name, descriptor)


class OdooModel(BaseModel, metaclass=OdooModelMeta):
    """Base class for all Odoo models with Pydantic validation.

    This class provides the foundation for type-safe Odoo record handling,
    including field validation, relationship management, and lazy loading.

    Features:
    - Type-safe field access with IDE support
    - Automatic validation of field values
    - Lazy loading for relationship fields
    - Integration with OdooFlow client
    - Serialization to/from Odoo data formats

    Example:
        >>> class ResPartner(OdooModel):
        ...     _odoo_name: ClassVar[str] = "res.partner"
        ...
        ...     name: str
        ...     email: Optional[str] = None
        ...     is_company: bool = False
        ...
        >>> partner = ResPartner(id=1, name="Test Company", is_company=True)
        >>> partner.name
        'Test Company'
    """

    model_config = ConfigDict(
        # Enable ORM mode for compatibility with Odoo data
        from_attributes=True,
        # Validate assignments to catch errors early
        validate_assignment=True,
        # Allow arbitrary types for complex fields
        arbitrary_types_allowed=True,
        # Use enum values instead of enum objects
        use_enum_values=True,
        # Populate by name for field aliases
        populate_by_name=True,
    )

    # Core Odoo fields that every record has
    id: int = Field(description="Unique record identifier")

    # Model metadata (excluded from serialization)
    odoo_name: ClassVar[str] = ""
    client: Optional[Any] = Field(default=None, exclude=True, repr=False)
    loaded_fields: set[str] = Field(default_factory=set, exclude=True, repr=False)
    relationship_manager: Optional[RelationshipManager] = Field(
        default=None, exclude=True, repr=False
    )

    def __init__(self, **data: Any):
        """Initialize the model with data from Odoo."""
        # Extract client if provided
        client = data.pop("client", None)

        super().__init__(**data)

        # Set client and initialize relationship manager
        if client:
            self.client = client
            self.relationship_manager = RelationshipManager(self, client)

        # Initialize relationship cache
        self._loaded_relationships = {}

        # Track which fields were loaded from the data
        self.loaded_fields = set(data.keys())

        # Initialize relationship manager
        if self.client:
            self.relationship_manager = RelationshipManager(self, self.client)

        # Track which fields were loaded
        self.loaded_fields = set(data.keys())

    @classmethod
    def get_odoo_name(cls) -> str:
        """Get the Odoo model name for this class.

        Returns:
            The Odoo model name (e.g., "res.partner")
        """
        return getattr(cls, "odoo_name", cls.__name__.lower())

    @classmethod
    def get_field_info(cls, field_name: str) -> Optional[FieldInfo]:
        """Get field information for a specific field.

        Args:
            field_name: Name of the field

        Returns:
            FieldInfo object or None if field doesn't exist
        """
        return cls.model_fields.get(field_name)

    @classmethod
    def get_relationship_fields(cls) -> Dict[str, FieldInfo]:
        """Get all relationship fields (Many2one, One2many, Many2many).

        Returns:
            Dictionary of field names to FieldInfo objects
        """
        relationship_fields = {}
        for field_name, field_info in cls.model_fields.items():
            # Check if field is a relationship type
            if hasattr(field_info.annotation, "__origin__"):
                # Handle Optional[RelationshipType] and List[RelationshipType]
                args = getattr(field_info.annotation, "__args__", ())
                if args and hasattr(args[0], "_odoo_name"):
                    relationship_fields[field_name] = field_info
            elif hasattr(field_info.annotation, "_odoo_name"):
                # Direct relationship type
                relationship_fields[field_name] = field_info

        return relationship_fields

    def __getattribute__(self, name: str) -> Any:
        """Override attribute access to implement lazy loading.

        This method intercepts field access to implement lazy loading
        for relationship fields that haven't been loaded yet.
        """
        # Get the value normally first
        value = super().__getattribute__(name)

        # Return LazyRelationship as-is, don't auto-load
        return value

    def __setattr__(self, name: str, value: Any) -> None:
        """Override attribute setting to track field changes."""
        super().__setattr__(name, value)

        # Track that this field has been loaded/modified
        if hasattr(self, "loaded_fields") and name in self.model_fields:
            self.loaded_fields.add(name)

    def is_field_loaded(self, field_name: str) -> bool:
        """Check if a field has been loaded from the server.

        Args:
            field_name: Name of the field to check

        Returns:
            True if the field has been loaded, False otherwise
        """
        return field_name in self.loaded_fields

    def get_loaded_fields(self) -> set[str]:
        """Get the set of fields that have been loaded.

        Returns:
            Set of field names that have been loaded
        """
        return self.loaded_fields.copy()

    def to_odoo_dict(self, exclude_unset: bool = True) -> Dict[str, Any]:
        """Convert the model to a dictionary suitable for Odoo operations.

        Args:
            exclude_unset: Whether to exclude fields that haven't been set

        Returns:
            Dictionary representation suitable for Odoo RPC calls
        """
        data = self.model_dump(exclude_unset=exclude_unset, exclude={"id"})

        # Convert relationship fields to appropriate format
        for field_name, field_info in self.get_relationship_fields().items():
            if field_name in data:
                value = data[field_name]
                # Convert based on relationship type
                # This will be expanded when we implement specific field types
                if isinstance(value, list):
                    # Many2many or One2many - convert to IDs
                    data[field_name] = [
                        item.id if hasattr(item, "id") else item for item in value
                    ]
                elif hasattr(value, "id"):
                    # Many2one - convert to ID
                    data[field_name] = value.id

        return data

    def refresh(self, fields: Optional[List[str]] = None) -> None:
        """Refresh the record data from the server.

        Args:
            fields: Specific fields to refresh, or None for all fields
        """
        if not self.client:
            raise ValueError("Cannot refresh record without client connection")

        # This will be implemented when we have the query builder
        # For now, it's a placeholder
        pass

    def save(self) -> None:
        """Save changes to the server.

        This method will save any modified fields back to the Odoo server.
        """
        if not self.client:
            raise ValueError("Cannot save record without client connection")

        # This will be implemented when we have the query builder
        # For now, it's a placeholder
        pass

    def __repr__(self) -> str:
        """String representation of the model."""
        class_name = self.__class__.__name__
        if hasattr(self, "name") and self.name:
            return f"{class_name}(id={self.id}, name='{self.name}')"
        return f"{class_name}(id={self.id})"

    def __str__(self) -> str:
        """Human-readable string representation."""
        if hasattr(self, "name") and self.name:
            return f"{self.name}"
        return f"{self.__class__.__name__}({self.id})"


class OdooRecord(OdooModel):
    """Alias for OdooModel for backward compatibility."""

    pass
