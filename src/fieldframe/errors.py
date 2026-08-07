"""FieldFrame semantic errors."""


class FieldFrameError(Exception):
    """Base exception for FieldFrame."""


class SemanticError(FieldFrameError):
    """An operation has no valid semantic interpretation."""


class InvariantViolation(FieldFrameError):
    """A Field invariant was violated."""


class UndefinedOperation(SemanticError):
    """No semantic rule exists for an operation over the supplied Fields."""


class ContextualValidationError(InvariantViolation):
    """A semantically valid transformation violates contextual invariants."""
