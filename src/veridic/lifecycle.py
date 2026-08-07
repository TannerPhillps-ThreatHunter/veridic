"""Knowledge lifecycle semantics.

Knowledge content and Knowledge lifecycle are distinct.

Knowledge contains:

    identity
    proposition
    warrant

Lifecycle records how the usability of that Knowledge changes.

Lifecycle history is append-only.

Current state is derived from the latest transition rather than stored
inside the Knowledge item itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class KnowledgeState(str, Enum):
    ACTIVE = "active"
    STALE = "stale"
    INVALID = "invalid"
    RETRACTED = "retracted"


@dataclass(frozen=True, slots=True)
class KnowledgeTransition:
    """One immutable lifecycle transition."""

    sequence: int
    knowledge: str
    from_state: KnowledgeState | None
    to_state: KnowledgeState
    reason: str
    cause: str | None = None

    def __post_init__(self) -> None:
        if self.sequence < 1:
            raise ValueError(
                "Transition sequence must be positive"
            )

        if not self.knowledge:
            raise ValueError(
                "Transition requires Knowledge identity"
            )

        if not self.reason:
            raise ValueError(
                "Transition requires reason"
            )

        if (
            self.from_state is not None
            and self.from_state is self.to_state
        ):
            raise ValueError(
                "Lifecycle transition must change state"
            )


__all__ = [
    "KnowledgeState",
    "KnowledgeTransition",
]
