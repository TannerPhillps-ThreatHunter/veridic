"""Veridic.

Experimental field-aware semantic DataFrame research runtime.
"""

from .dimensions import SemanticDimension
from .domain_law import DomainLaw
from .domain_laws import DOMAIN_LAWS, build_domain_runtime
from .errors import (
    VeridicError,
    InvariantViolation,
    SemanticError,
    UndefinedOperation,
)
from .execution import ExecutionResult, execute
from .field import Field, FieldValue
from .hierarchy import (
    Classification,
    ClassificationError,
    ClassificationRegistry,
    DuplicateClassification,
    UnknownCategory,
    UnknownKind,
    UnknownType,
)
from .invariant import Invariant, InvariantScope
from .record import SemanticRecord
from .rules import build_runtime
from .runtime import Admission, SemanticRuntime
from .taxonomy import DEFAULT_CLASSIFICATION_REGISTRY
from .validation import (
    InvariantCheck,
    ValidationReport,
    validate_field_value,
    validate_record,
)
from .vocabulary import Operation, Scale, ValidityLevel

__all__ = [
    "DEFAULT_CLASSIFICATION_REGISTRY",
    "DOMAIN_LAWS",
    "Admission",
    "Classification",
    "ClassificationError",
    "ClassificationRegistry",
    "DomainLaw",
    "DuplicateClassification",
    "ExecutionResult",
    "Field",
    "VeridicError",
    "FieldValue",
    "Invariant",
    "InvariantCheck",
    "InvariantScope",
    "InvariantViolation",
    "Operation",
    "Scale",
    "SemanticDimension",
    "SemanticError",
    "SemanticRecord",
    "SemanticRuntime",
    "UndefinedOperation",
    "UnknownCategory",
    "UnknownKind",
    "UnknownType",
    "ValidationReport",
    "ValidityLevel",
    "build_domain_runtime",
    "build_runtime",
    "execute",
    "validate_field_value",
    "validate_record",
]

__version__ = "0.2.0"
