"""Inspection helpers for domain-law evidence."""

from __future__ import annotations

from collections import defaultdict

from .dimensions import SemanticDimension
from .domain_laws import DOMAIN_LAWS


def dimension_usage() -> dict[SemanticDimension, tuple[str, ...]]:
    """Return domain laws grouped by Field dimension dependency."""

    usage: dict[SemanticDimension, list[str]] = defaultdict(list)

    for law in DOMAIN_LAWS:
        for dimension in law.depends_on:
            usage[dimension].append(law.name)

    return {
        dimension: tuple(sorted(names))
        for dimension, names in usage.items()
    }
