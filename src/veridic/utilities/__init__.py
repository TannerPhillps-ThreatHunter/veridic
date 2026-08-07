"""Veridic native utilities.

Utilities are foundational computational primitives owned by Veridic.

They are not a miscellaneous helper namespace.

Every utility subsystem must correspond to an explicit semantic or
computational responsibility.
"""

from .truth import Truth

__all__ = [
    "Truth",
]
