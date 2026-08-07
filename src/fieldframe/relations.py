"""Relations preserved by measurement scales."""

from __future__ import annotations

from enum import Enum

from .vocabulary import Scale


class Relation(str, Enum):
    EQUALITY = "equality"
    ORDER = "order"
    DIFFERENCE = "difference"
    RATIO = "ratio"


_SCALE_RELATIONS: dict[Scale, frozenset[Relation]] = {
    Scale.NOMINAL: frozenset(
        {
            Relation.EQUALITY,
        }
    ),
    Scale.ORDINAL: frozenset(
        {
            Relation.EQUALITY,
            Relation.ORDER,
        }
    ),
    Scale.INTERVAL: frozenset(
        {
            Relation.EQUALITY,
            Relation.ORDER,
            Relation.DIFFERENCE,
        }
    ),
    Scale.RATIO: frozenset(
        {
            Relation.EQUALITY,
            Relation.ORDER,
            Relation.DIFFERENCE,
            Relation.RATIO,
        }
    ),
}


def relations_for(scale: Scale) -> frozenset[Relation]:
    return _SCALE_RELATIONS[scale]


def supports(scale: Scale, relation: Relation) -> bool:
    return relation in relations_for(scale)
