"""Central Bank Intelligence Engine (CENT-001) – NRES Compliant."""

__version__ = "1.0.0"

from .acquisition import CentralBankCollector
from .warehouse import CentralBankWarehouse

# Gateways and publishers are optional; import only if needed
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
    "CentralBankWarehouse",
    "CentralBankGateway",
    "CentralBankPublisher",
]
