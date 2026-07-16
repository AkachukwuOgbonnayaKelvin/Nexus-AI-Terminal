"""Financial News Engine (NEWS-001) – NRES Compliant."""

from .acquisition import NewsCollector
from .gateway import NewsGateway
from .warehouse import NewsWarehouse

__all__ = ["NewsCollector", "NewsWarehouse", "NewsGateway"]
