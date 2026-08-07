from veridic.utilities.testing import raises
from veridic.utilities.units import (
    BYTE,
    DEFAULT_UNIT_REGISTRY,
    SECOND,
    DuplicateUnit,
    UnitRegistry,
    UnknownUnit,
)


def test_registry_resolves_name():
    assert (
        DEFAULT_UNIT_REGISTRY.resolve(
            "second"
        )
        is SECOND
    )


def test_registry_resolves_symbol():
    assert (
        DEFAULT_UNIT_REGISTRY.resolve(
            "B"
        )
        is BYTE
    )


def test_unknown_unit_rejected():
    with raises(UnknownUnit):
        DEFAULT_UNIT_REGISTRY.resolve(
            "furlong_per_fortnight"
        )


def test_duplicate_unit_rejected():
    registry = UnitRegistry()

    registry.register(
        SECOND
    )

    with raises(DuplicateUnit):
        registry.register(
            SECOND
        )
