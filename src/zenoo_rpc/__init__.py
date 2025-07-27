"""
Zenoo-RPC: A zen-like, modern async Python library for Odoo RPC with type
safety and superior DX.

This library provides a zen-like, elegant alternative to odoorpc with the
following key features:
- Async-first design with httpx
- Type safety with Pydantic models
- Fluent query builder
- Intelligent caching with TTL/LRU strategies
- Transaction management with ACID compliance
- Batch operations for high performance
- Structured exception handling
- Enhanced connection pooling with HTTP/2
"""

from .client import ZenooClient
from .exceptions import (
    ZenooError,
    ConnectionError,
    AuthenticationError,
    ValidationError,
    AccessError,
    TimeoutError,
)

# Import models and query components
from .models.base import OdooModel
from .models.registry import register_model, get_model_class
from .query import QueryBuilder, Q, Field

# Import common models
from .models.common import (
    ResPartner,
    ResCountry,
    ResCountryState,
    ResCurrency,
    ResUsers,
    ResGroups,
    ProductProduct,
    ProductCategory,
    SaleOrder,
    SaleOrderLine,
)

__version__ = "0.1.0"
__author__ = "Lê Anh Tuấn"
__email__ = "justin.le.1105@gmail.com"

__all__ = [
    # Core client
    "ZenooClient",
    # Exceptions
    "ZenooError",
    "ConnectionError",
    "AuthenticationError",
    "ValidationError",
    "AccessError",
    "TimeoutError",
    # Models and registry
    "OdooModel",
    "register_model",
    "get_model_class",
    # Query building
    "QueryBuilder",
    "Q",
    "Field",
    # Common models
    "ResPartner",
    "ResCountry",
    "ResCountryState",
    "ResCurrency",
    "ResUsers",
    "ResGroups",
    "ProductProduct",
    "ProductCategory",
    "SaleOrder",
    "SaleOrderLine",
]
