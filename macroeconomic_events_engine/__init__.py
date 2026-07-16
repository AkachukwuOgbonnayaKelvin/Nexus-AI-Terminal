"""Macroeconomic Events Engine (MAC-002) – NERS compliant."""

from .acquisition import MacroCollector
from .services import MacroService
from .warehouse import ConsensusWarehouse, RawWarehouse

__all__ = ["MacroCollector", "RawWarehouse", "ConsensusWarehouse", "MacroService"]
