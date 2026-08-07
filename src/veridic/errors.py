"""Veridic semantic errors."""


class VeridicError(Exception):
    """Base exception for Veridic."""


class SemanticError(VeridicError):
    """An operation has no valid semantic interpretation."""


class InvariantViolation(VeridicError):
    """A Field invariant was violated."""


class UndefinedOperation(SemanticError):
    """No semantic rule exists for an operation over the supplied Fields."""


class ContextualValidationError(InvariantViolation):
    """A semantically valid transformation violates contextual invariants."""
