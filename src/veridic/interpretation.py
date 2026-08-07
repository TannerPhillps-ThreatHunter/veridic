"""Truth evaluation boundary.

A Proposition is truth-apt Information.

Its presence in Veridic does not establish its Truth.

Truth is produced only by evaluation under an Interpretation:

    Proposition + Interpretation -> Truth
"""

from __future__ import annotations

from typing import Protocol

from .information import Proposition
from .utilities.truth import Truth


class Interpretation(Protocol):
    """Something capable of evaluating a Proposition."""

    def evaluate(
        self,
        proposition: Proposition,
    ) -> Truth:
        """Evaluate a Proposition under this Interpretation."""


def evaluate_truth(
    proposition: Proposition,
    *,
    under: Interpretation,
) -> Truth:
    """Evaluate truth explicitly under an Interpretation."""

    result = under.evaluate(
        proposition
    )

    if not isinstance(
        result,
        Truth,
    ):
        raise TypeError(
            "Interpretation.evaluate() must return Truth"
        )

    return result


__all__ = [
    "Interpretation",
    "evaluate_truth",
]
