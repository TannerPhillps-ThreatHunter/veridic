"""Executable Field invariant primitives."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Any


class InvariantScope(str, Enum):
    """Scope over which an invariant makes a semantic claim."""

    VALUE = "value"
    FIELD = "field"
    RELATIONAL = "relational"
    STRUCTURAL = "structural"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class Invariant:
    """A semantic obligation that must remain true.

    An invariant may be:

        executable
            predicate is available and required context exists;

        unresolved
            predicate exists but required context is unavailable;

        declarative
            no executable predicate exists yet.

    This distinction prevents lack of evidence from silently becoming
    either success or failure.
    """

    name: str
    expression: str
    scope: InvariantScope = InvariantScope.FIELD

    predicate: Callable[[Mapping[str, Any]], bool] | None = None

    required_keys: tuple[str, ...] = ()

    def evaluate(
        self,
        context: Mapping[str, Any],
    ) -> bool | None:
        """Evaluate the invariant when sufficient evidence exists.

        Returns:
            True
                invariant was executable and satisfied;

            False
                invariant was executable and violated;

            None
                invariant cannot currently be evaluated.
        """

        if self.predicate is None:
            return None

        if any(
            key not in context
            for key in self.required_keys
        ):
            return None

        return bool(self.predicate(context))
