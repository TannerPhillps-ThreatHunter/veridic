"""FieldFrame.

Experimental field-aware semantic DataFrame research runtime.
"""

from .errors import (
    FieldFrameError,
    InvariantViolation,
    SemanticError,
    UndefinedOperation,
)
from .field import Classification, Field, FieldValue
from .invariant import Invariant, InvariantScope
from .rules import build_runtime
from .runtime import Admission, SemanticRuntime
from .vocabulary import Operation, Scale, ValidityLevel

__all__ = [
    "Admission",
    "Classification",
    "Field",
    "FieldFrameError",
    "FieldValue",
    "Invariant",
    "InvariantScope",
    "InvariantViolation",
    "Operation",
    "Scale",
    "SemanticError",
    "SemanticRuntime",
    "UndefinedOperation",
    "ValidityLevel",
    "build_runtime",
]

__version__ = "0.1.0"
