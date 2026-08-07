"""Epistemic support calculus.

Truth and epistemic support answer different questions.

Truth asks:

    Is proposition P true?

Support asks:

    What active warranted Knowledge supports P?
    What active warranted Knowledge supports NOT P?

Support is represented as two independent dimensions:

    support_for
    support_against

This produces four possible states without introducing a fourth truth
value:

    NEITHER
    FOR
    AGAINST
    BOTH

BOTH means that P and NOT P each possess active warrant.

It does not mean that Veridic has declared P objectively both true and
false.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .information import Proposition


class SupportState(str, Enum):
    """Derived epistemic support state."""

    NEITHER = "neither"
    FOR = "for"
    AGAINST = "against"
    BOTH = "both"


@dataclass(frozen=True, slots=True)
class EpistemicSupport:
    """Warrant support surrounding one Proposition."""

    proposition: Proposition

    for_knowledge: tuple[str, ...] = ()
    against_knowledge: tuple[str, ...] = ()

    @property
    def has_support_for(self) -> bool:
        return bool(
            self.for_knowledge
        )

    @property
    def has_support_against(self) -> bool:
        return bool(
            self.against_knowledge
        )

    @property
    def state(self) -> SupportState:
        positive = (
            self.has_support_for
        )

        negative = (
            self.has_support_against
        )

        if positive and negative:
            return SupportState.BOTH

        if positive:
            return SupportState.FOR

        if negative:
            return SupportState.AGAINST

        return SupportState.NEITHER

    @property
    def contested(self) -> bool:
        return (
            self.state
            is SupportState.BOTH
        )

    @property
    def unsupported(self) -> bool:
        return (
            self.state
            is SupportState.NEITHER
        )


__all__ = [
    "EpistemicSupport",
    "SupportState",
]
