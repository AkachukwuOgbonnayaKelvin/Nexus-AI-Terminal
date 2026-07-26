"""Central Bank Intelligence Engine (CENT-001)."""

__version__ = "1.0.0"

# Import only what actually exists
try:
    from .acquisition import CentralBankCollector
except ImportError:
    CentralBankCollector = None

try:
    from .warehouse import CentralBankWarehouse
except ImportError:
    CentralBankWarehouse = None

try:
    from .gateway import CentralBankGateway
except ImportError:
    CentralBankGateway = None

try:
    from .publication import CentralBankPublisher
except ImportError:
    CentralBankPublisher = None

__all__ = [
    "CentralBankCollector",
    "CentralBankGateway",
    "CentralBankPublisher",
    "CentralBankWarehouse",
]
