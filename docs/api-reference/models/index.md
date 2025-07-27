# Models API Reference

The models module provides type-safe, Pydantic-based representations of Odoo models with automatic validation, relationship handling, and ORM-like functionality.

## Overview

Zenoo RPC models offer:

- **Type Safety**: Full type hints and IDE support
- **Validation**: Automatic data validation with Pydantic
- **Relationships**: Lazy loading and relationship management
- **Registry**: Dynamic model registration and discovery
- **Field Types**: Specialized field types for Odoo data

## Base Classes

### `OdooModel`

Base class for all Odoo model representations.

```python
from zenoo_rpc.models.base import OdooModel
from typing import Optional, ClassVar

class CustomModel(OdooModel):
    _odoo_name: ClassVar[str] = "custom.model"
    
    name: str
    description: Optional[str] = None
    active: bool = True
```

**Key Features:**

- Inherits from Pydantic `BaseModel`
- Automatic field validation
- JSON serialization/deserialization
- Relationship field support
- Computed properties

**Class Variables:**

- `_odoo_name`: Odoo model name (required)
- `_odoo_fields`: Field definitions (auto-generated)
- `_relationships`: Relationship field mappings

### `OdooRecord`

Enhanced model with client integration for active record pattern.

```python
from zenoo_rpc.models.base import OdooRecord

class ActivePartner(OdooRecord):
    _odoo_name: ClassVar[str] = "res.partner"
    
    name: str
    email: Optional[str] = None
    
    async def save(self):
        """Save changes to Odoo."""
        if self.id:
            await self._client.write(self._odoo_name, [self.id], self.dict())
        else:
            self.id = await self._client.create(self._odoo_name, self.dict())
    
    async def delete(self):
        """Delete record from Odoo."""
        if self.id:
            await self._client.unlink(self._odoo_name, [self.id])
```

## Common Models

### `ResPartner`

Partner/Customer model with comprehensive field definitions.

```python
from zenoo_rpc.models.common import ResPartner
from zenoo_rpc.models.fields import Many2OneField

class ResPartner(OdooModel):
    _odoo_name: ClassVar[str] = "res.partner"
    
    # Basic fields
    id: Optional[int] = None
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    website: Optional[str] = None
    
    # Boolean fields
    is_company: bool = False
    active: bool = True
    
    # Ranking fields
    customer_rank: int = 0
    supplier_rank: int = 0
    
    # Address fields
    street: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    
    # Relationship fields
    country_id: Optional[Many2OneField["ResCountry"]] = None
    state_id: Optional[Many2OneField["ResCountryState"]] = None
    parent_id: Optional[Many2OneField["ResPartner"]] = None
    
    # Computed properties
    @property
    def is_customer(self) -> bool:
        """Check if partner is a customer."""
        return self.customer_rank > 0
    
    @property
    def is_supplier(self) -> bool:
        """Check if partner is a supplier."""
        return self.supplier_rank > 0
    
    @property
    def display_name(self) -> str:
        """Get display name for partner."""
        return self.name or f"Partner #{self.id}"
```

**Usage Examples:**

```python
# Create partner instance
partner = ResPartner(
    name="ACME Corporation",
    email="contact@acme.com",
    is_company=True,
    customer_rank=1
)

# Access computed properties
if partner.is_customer:
    print(f"{partner.display_name} is a customer")

# Validate data
try:
    invalid_partner = ResPartner(name="", email="invalid-email")
except ValidationError as e:
    print(f"Validation failed: {e}")
```

### `ResCountry`

Country model for address management.

```python
from zenoo_rpc.models.common import ResCountry

class ResCountry(OdooModel):
    _odoo_name: ClassVar[str] = "res.country"
    
    id: Optional[int] = None
    name: str
    code: str  # ISO country code
    phone_code: Optional[int] = None
    currency_id: Optional[Many2OneField["ResCurrency"]] = None
```

### `ResUsers`

User model for authentication and permissions.

```python
from zenoo_rpc.models.common import ResUsers

class ResUsers(OdooModel):
    _odoo_name: ClassVar[str] = "res.users"
    
    id: Optional[int] = None
    name: str
    login: str
    email: Optional[str] = None
    active: bool = True
    
    # Relationship to partner
    partner_id: Optional[Many2OneField["ResPartner"]] = None
    
    # Groups and permissions
    groups_id: Optional[Many2ManyField["ResGroups"]] = None
```

## Field Types

### `Many2OneField`

Represents a many-to-one relationship.

```python
from zenoo_rpc.models.fields import Many2OneField

class OrderLine(OdooModel):
    _odoo_name: ClassVar[str] = "sale.order.line"
    
    order_id: Many2OneField["SaleOrder"]
    product_id: Many2OneField["ProductProduct"]
    
    async def get_order(self) -> "SaleOrder":
        """Get related order."""
        return await self.order_id
    
    async def get_product(self) -> "ProductProduct":
        """Get related product."""
        return await self.product_id
```

### `One2ManyField`

Represents a one-to-many relationship.

```python
from zenoo_rpc.models.fields import One2ManyField

class SaleOrder(OdooModel):
    _odoo_name: ClassVar[str] = "sale.order"
    
    name: str
    order_line: One2ManyField["SaleOrderLine"]
    
    async def get_lines(self) -> List["SaleOrderLine"]:
        """Get all order lines."""
        return await self.order_line
```

### `Many2ManyField`

Represents a many-to-many relationship.

```python
from zenoo_rpc.models.fields import Many2ManyField

class ResPartner(OdooModel):
    _odoo_name: ClassVar[str] = "res.partner"
    
    name: str
    category_id: Many2ManyField["ResPartnerCategory"]
    
    async def get_categories(self) -> List["ResPartnerCategory"]:
        """Get all partner categories."""
        return await self.category_id
```

### `SelectionField`

Represents a selection field with predefined choices.

```python
from zenoo_rpc.models.fields import SelectionField

class SaleOrder(OdooModel):
    _odoo_name: ClassVar[str] = "sale.order"
    
    state: SelectionField = SelectionField(
        choices=[
            ("draft", "Draft"),
            ("sent", "Quotation Sent"),
            ("sale", "Sales Order"),
            ("done", "Locked"),
            ("cancel", "Cancelled")
        ],
        default="draft"
    )
```

### `DateField` and `DateTimeField`

Date and datetime fields with proper Python types.

```python
from zenoo_rpc.models.fields import DateField, DateTimeField
from datetime import date, datetime

class SaleOrder(OdooModel):
    _odoo_name: ClassVar[str] = "sale.order"
    
    date_order: DateTimeField
    commitment_date: Optional[DateField] = None
    
    @property
    def is_recent(self) -> bool:
        """Check if order is from last 30 days."""
        if not self.date_order:
            return False
        return (datetime.now() - self.date_order).days <= 30
```

## Model Registry

### `register_model()`

Register a custom model with the registry.

```python
from zenoo_rpc.models.registry import register_model

@register_model
class CustomModel(OdooModel):
    _odoo_name: ClassVar[str] = "custom.model"
    
    name: str
    description: Optional[str] = None
```

### `get_model_class()`

Get a model class by Odoo model name.

```python
from zenoo_rpc.models.registry import get_model_class

# Get registered model class
PartnerClass = get_model_class("res.partner")
if PartnerClass:
    partner = PartnerClass(name="Test Partner")
```

## Relationship Management

### Lazy Loading

Relationships are loaded lazily when accessed.

```python
# Partner with country relationship
partner = await client.model(ResPartner).filter(id=1).first()

# Country is loaded when accessed
country = await partner.country_id  # Triggers database query
print(country.name)

# Subsequent access uses cached value
country_again = await partner.country_id  # No database query
```

### Prefetching

Load relationships efficiently with prefetching.

```python
# Prefetch related data
partners = await client.model(ResPartner).filter(
    is_company=True
).prefetch_related("country_id", "state_id").all()

# No additional queries needed
for partner in partners:
    country = await partner.country_id  # Already loaded
    state = await partner.state_id      # Already loaded
```

## Validation

### Field Validation

Models automatically validate field values using Pydantic.

```python
try:
    # This will raise ValidationError
    partner = ResPartner(
        name="",  # Empty name
        email="invalid-email",  # Invalid email format
        customer_rank=-1  # Negative rank
    )
except ValidationError as e:
    for error in e.errors():
        print(f"Field {error['loc']}: {error['msg']}")
```

### Custom Validators

Add custom validation logic to models.

```python
from pydantic import validator

class ResPartner(OdooModel):
    _odoo_name: ClassVar[str] = "res.partner"
    
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()
    
    @validator('email')
    def email_must_be_valid(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('phone')
    def phone_must_be_valid(cls, v):
        if v and len(v) < 10:
            raise ValueError('Phone number too short')
        return v
```

## Serialization

### JSON Serialization

Models can be serialized to/from JSON.

```python
# Create partner
partner = ResPartner(
    name="ACME Corp",
    email="contact@acme.com",
    is_company=True
)

# Serialize to JSON
json_data = partner.json()
print(json_data)

# Serialize to dict
dict_data = partner.dict()
print(dict_data)

# Create from JSON
partner_from_json = ResPartner.parse_raw(json_data)

# Create from dict
partner_from_dict = ResPartner(**dict_data)
```

### Odoo Format

Convert between Zenoo models and Odoo data format.

```python
# From Odoo data
odoo_data = {
    "id": 1,
    "name": "ACME Corp",
    "email": "contact@acme.com",
    "is_company": True,
    "country_id": [1, "United States"]  # Odoo format
}

partner = ResPartner.from_odoo_data(odoo_data)

# To Odoo format
odoo_format = partner.to_odoo_data()
```

## Advanced Usage

### Dynamic Models

Create models dynamically for custom Odoo models.

```python
from zenoo_rpc.models.base import create_dynamic_model

# Create model for custom Odoo model
CustomModel = create_dynamic_model(
    "custom.model",
    {
        "name": str,
        "description": Optional[str],
        "active": bool
    }
)

# Use like any other model
instance = CustomModel(name="Test", active=True)
```

### Model Inheritance

Extend existing models with additional functionality.

```python
class ExtendedPartner(ResPartner):
    """Extended partner with additional methods."""
    
    def get_full_address(self) -> str:
        """Get formatted full address."""
        parts = [
            self.street,
            self.street2,
            self.city,
            self.zip
        ]
        return ", ".join(filter(None, parts))
    
    async def get_orders(self, client: ZenooClient) -> List["SaleOrder"]:
        """Get all orders for this partner."""
        if not self.id:
            return []
        
        return await client.model(SaleOrder).filter(
            partner_id=self.id
        ).all()
```

## Performance Considerations

### Field Selection

Only load needed fields to improve performance.

```python
# Load only specific fields
partners = await client.model(ResPartner).only(
    "name", "email", "phone"
).filter(is_company=True).all()
```

### Batch Loading

Use batch operations for multiple model instances.

```python
# Batch create
partners_data = [
    {"name": "Company 1", "email": "c1@test.com"},
    {"name": "Company 2", "email": "c2@test.com"}
]

created_ids = await client.batch_manager.bulk_create(
    model="res.partner",
    records=partners_data
)
```

### Caching

Cache frequently accessed model data.

```python
# Cache model queries
countries = await client.model(ResCountry).cache(
    key="all_countries",
    ttl=3600
).all()
```

## Next Steps

- Explore [Query Building](../query/index.md) for advanced querying
- Learn about [Field Types](fields.md) in detail
- Check [Relationship Management](relationships.md) patterns
