"""Validator Registry – Lists all architecture validators."""

from pathlib import Path
from typing import List, Type
from tools.architecture.validators.base import BaseValidator

# Core validators
from tools.architecture.validators.engine_structure import EngineStructureValidator
from tools.architecture.validators.import_validator import ImportValidator
from tools.architecture.validators.runtime_validator import RuntimeValidator

# Structural validators
from tools.architecture.validators.structural.blueprint import BlueprintValidator
from tools.architecture.validators.structural.import_boundary import (
    ImportBoundaryValidator,
)
from tools.architecture.validators.structural.dependency_graph import (
    DependencyGraphValidator,
)

# Other validators
from tools.architecture.validators.init_validator import InitValidator
from tools.architecture.validators.naming_validator import NamingValidator
from tools.architecture.validators.circular_validator import CircularValidator
from tools.architecture.validators.folder_validator import FolderValidator
from tools.architecture.validators.publication_validator import PublicationValidator
from tools.architecture.validators.warehouse_validator import WarehouseValidator
from tools.architecture.validators.ndip_validator import NDIPValidator
from tools.architecture.validators.provider_validator import ProviderValidator
from tools.architecture.validators.historical_validator import HistoricalValidator
from tools.architecture.validators.engine_contract_validator import (
    EngineContractValidator,
)
from tools.architecture.validators.schema_validator import SchemaValidator
from tools.architecture.validators.health_validator import HealthValidator

# Registry of all validators
VALIDATOR_CLASSES: List[Type[BaseValidator]] = [
    # Core
    EngineStructureValidator,
    ImportValidator,
    RuntimeValidator,
    # Structural
    BlueprintValidator,
    ImportBoundaryValidator,
    DependencyGraphValidator,
    # Others
    InitValidator,
    NamingValidator,
    CircularValidator,
    FolderValidator,
    PublicationValidator,
    WarehouseValidator,
    NDIPValidator,
    ProviderValidator,
    HistoricalValidator,
    EngineContractValidator,
    SchemaValidator,
    HealthValidator,
]


def get_validators(root_path: Path) -> List[BaseValidator]:
    """Instantiate all validators."""
    return [vc(root_path) for vc in VALIDATOR_CLASSES]
