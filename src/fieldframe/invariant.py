"""Field invariant primitives."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Any


class InvariantScope(str, Enum):
    VALUE = "value"
    FIELD = "field"
    RELATIONAL = "relational"
    STRUCTURAL = "structural"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class Invariant:
    """A semantic obligation that must remain true.

    `predicate` is intentionally optional. Some invariants may initially
    exist as declarative semantic statements before they become executable.
    """

    name: str
    expression: str
    scope: InvariantScope = InvariantScope.FIELD
    predicate: Callable[[Mapping[str, Any]], bool] | None = None

    def evaluate(self, context: Mapping[str, Any]) -> bool | None:
        """Evaluate the invariant when executable.

        Returns:
            True / False when a predicate exists.
            None when the invariant is declarative only.
        """
        if self.predicate is None:
            return None

        return bool(self.predicate(context))
