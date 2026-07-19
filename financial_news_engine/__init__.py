"""Financial News Engine (NEWS-001)."""

__version__ = "1.0.0"

try:
    from .acquisition import NewsCollector
except ImportError:
    NewsCollector = None

try:
    from .warehouse import NewsWarehouse
except ImportError:
    NewsWarehouse = None

try:
    from .gateway import NewsGateway
except ImportError:
    NewsGateway = None

__all__ = [
    "NewsCollector",
    "NewsWarehouse",
    "NewsGateway",
]
