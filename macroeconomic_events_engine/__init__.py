"""Macroeconomic Events Engine (MAC-002)."""

__version__ = "1.0.0"

try:
    from .acquisition import MacroCollector
except ImportError:
    MacroCollector = None

try:
    from .warehouse import ConsensusWarehouse, RawWarehouse
except ImportError:
    RawWarehouse = None
    ConsensusWarehouse = None

try:
    from .services import MacroService
except ImportError:
    MacroService = None

__all__ = [
    "MacroCollector",
    "RawWarehouse",
    "ConsensusWarehouse",
    "MacroService",
]
