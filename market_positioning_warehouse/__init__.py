"""Market Positioning Warehouse (INS-001)."""

__version__ = "1.0.0"

try:
    from .runtime import HistoricalImport, LifecycleManager, WeeklyScheduler
except ImportError:
    HistoricalImport = None
    WeeklyScheduler = None
    LifecycleManager = None

try:
    from .warehouse import Repository, WarehouseState
except ImportError:
    Repository = None
    WarehouseState = None

__all__ = [
    "HistoricalImport",
    "WeeklyScheduler",
    "LifecycleManager",
    "Repository",
    "WarehouseState",
]
