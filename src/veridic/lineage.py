"""Epistemic warrant lineage.

Warrant multiplicity is not equivalent to independent support.

Several Knowledge items may warrant the same Proposition while
ultimately depending upon the same asserted roots.

This module distinguishes:

    warrant count

from:

    lineage groups

A lineage group is a connected component of warrants whose assertion
root sets overlap.

This is deliberately narrower than full epistemic independence.

Disjoint assertion ancestry establishes lineage independence only.

It does not prove independence of:

    source
    sensor
    dataset
    observer
    causal mechanism
    organization
    upstream collection system

Those remain future problems.
"""

from __future__ import annotations

from dataclasses import dataclass

from .information import Proposition


@dataclass(frozen=True, slots=True)
class WarrantLineage:
    """Assertion-root ancestry for one Knowledge item."""

    knowledge: str
    assertion_roots: tuple[str, ...]

    @property
    def root_count(self) -> int:
        return len(
            self.assertion_roots
        )


@dataclass(frozen=True, slots=True)
class LineageGroup:
    """Warrants connected by shared assertion ancestry."""

    knowledge: tuple[str, ...]
    assertion_roots: tuple[str, ...]

    @property
    def warrant_count(self) -> int:
        return len(
            self.knowledge
        )

    @property
    def root_count(self) -> int:
        return len(
            self.assertion_roots
        )


def group_lineages(
    lineages: tuple[
        WarrantLineage,
        ...,
    ],
) -> tuple[
    LineageGroup,
    ...,
]:
    """Group warrants whose assertion-root ancestries overlap.

    Overlap is transitive.

    If:

        K1 shares root A with K2

    and:

        K2 shares root B with K3

    then K1, K2, and K3 belong to the same lineage group even if K1
    and K3 do not directly share a root.
    """

    remaining = list(
        lineages
    )

    groups: list[
        LineageGroup
    ] = []

    while remaining:
        seed = remaining.pop(
            0
        )

        members = {
            seed.knowledge
        }

        roots = set(
            seed.assertion_roots
        )

        changed = True

        while changed:
            changed = False

            survivors = []

            for lineage in remaining:
                lineage_roots = set(
                    lineage.assertion_roots
                )

                if roots.intersection(
                    lineage_roots
                ):
                    members.add(
                        lineage.knowledge
                    )

                    roots.update(
                        lineage_roots
                    )

                    changed = True
                else:
                    survivors.append(
                        lineage
                    )

            remaining = survivors

        groups.append(
            LineageGroup(
                knowledge=tuple(
                    sorted(
                        members
                    )
                ),
                assertion_roots=tuple(
                    sorted(
                        roots
                    )
                ),
            )
        )

    return tuple(
        sorted(
            groups,
            key=lambda group: (
                group.knowledge
            ),
        )
    )


@dataclass(frozen=True, slots=True)
class SupportLineage:
    """Lineage analysis around one Proposition."""

    proposition: Proposition

    for_lineages: tuple[
        WarrantLineage,
        ...,
    ] = ()

    against_lineages: tuple[
        WarrantLineage,
        ...,
    ] = ()

    @property
    def for_groups(
        self,
    ) -> tuple[
        LineageGroup,
        ...,
    ]:
        return group_lineages(
            self.for_lineages
        )

    @property
    def against_groups(
        self,
    ) -> tuple[
        LineageGroup,
        ...,
    ]:
        return group_lineages(
            self.against_lineages
        )

    @property
    def for_warrant_count(
        self,
    ) -> int:
        return len(
            self.for_lineages
        )

    @property
    def against_warrant_count(
        self,
    ) -> int:
        return len(
            self.against_lineages
        )

    @property
    def for_lineage_count(
        self,
    ) -> int:
        return len(
            self.for_groups
        )

    @property
    def against_lineage_count(
        self,
    ) -> int:
        return len(
            self.against_groups
        )

    @property
    def redundant_for_warrants(
        self,
    ) -> int:
        return (
            self.for_warrant_count
            - self.for_lineage_count
        )

    @property
    def redundant_against_warrants(
        self,
    ) -> int:
        return (
            self.against_warrant_count
            - self.against_lineage_count
        )


__all__ = [
    "LineageGroup",
    "SupportLineage",
    "WarrantLineage",
    "group_lineages",
]
