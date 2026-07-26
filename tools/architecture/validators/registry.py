"""Validator Registry – Lists all architecture validators."""

from pathlib import Path

from tools.architecture.validators.base import BaseValidator
from tools.architecture.validators.circular_validator import CircularValidator
from tools.architecture.validators.engine_contract_validator import (
    EngineContractValidator,
)

# Core validators
from tools.architecture.validators.engine_structure import EngineStructureValidator
from tools.architecture.validators.folder_validator import FolderValidator
from tools.architecture.validators.health_validator import HealthValidator
from tools.architecture.validators.historical_validator import HistoricalValidator
from tools.architecture.validators.import_validator import ImportValidator

# Other validators
from tools.architecture.validators.init_validator import InitValidator
from tools.architecture.validators.naming_validator import NamingValidator
from tools.architecture.validators.ndip_validator import NDIPValidator
from tools.architecture.validators.provider_validator import ProviderValidator
from tools.architecture.validators.publication_validator import PublicationValidator
from tools.architecture.validators.runtime_validator import RuntimeValidator
from tools.architecture.validators.schema_validator import SchemaValidator

# Structural validators
from tools.architecture.validators.structural.blueprint import BlueprintValidator
from tools.architecture.validators.structural.dependency_graph import (
    DependencyGraphValidator,
)
from tools.architecture.validators.structural.import_boundary import (
    ImportBoundaryValidator,
)
from tools.architecture.validators.warehouse_validator import WarehouseValidator

# Registry of all validators
VALIDATOR_CLASSES: list[type[BaseValidator]] = [
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


def get_validators(root_path: Path) -> list[BaseValidator]:
    """Instantiate all validators."""
    return [vc(root_path) for vc in VALIDATOR_CLASSES]
