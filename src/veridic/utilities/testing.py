"""Minimal testing primitives used by the Veridic test suite."""

from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator
from typing import TypeVar


E = TypeVar(
    "E",
    bound=BaseException,
)


@contextmanager
def raises(
    exception_type: type[E],
) -> Iterator[None]:
    """Assert that a block raises the requested exception."""

    try:
        yield
    except exception_type:
        return
    except BaseException as exc:
        raise AssertionError(
            "Expected "
            f"{exception_type.__name__}, "
            "but received "
            f"{type(exc).__name__}"
        ) from exc

    raise AssertionError(
        "Expected "
        f"{exception_type.__name__} "
        "to be raised"
    )
