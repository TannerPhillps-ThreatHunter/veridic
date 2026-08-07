"""FieldFrame.

Experimental field-aware semantic DataFrame research runtime.
"""

from .dimensions import SemanticDimension
from .domain_law import DomainLaw
from .domain_laws import DOMAIN_LAWS, build_domain_runtime
from .errors import (
    FieldFrameError,
    InvariantViolation,
    SemanticError,
    UndefinedOperation,
)
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
from .rules import build_runtime
from .runtime import Admission, SemanticRuntime
from .taxonomy import DEFAULT_CLASSIFICATION_REGISTRY
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
    "Field",
    "FieldFrameError",
    "FieldValue",
    "Invariant",
    "InvariantScope",
    "InvariantViolation",
    "Operation",
    "Scale",
    "SemanticDimension",
    "SemanticError",
    "SemanticRuntime",
    "UndefinedOperation",
    "UnknownCategory",
    "UnknownKind",
    "UnknownType",
    "ValidityLevel",
    "build_domain_runtime",
    "build_runtime",
]

__version__ = "0.1.0"
