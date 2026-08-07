from veridic.utilities.testing import raises

from veridic.hierarchy import (
    Classification,
    ClassificationRegistry,
    DuplicateClassification,
    UnknownCategory,
    UnknownKind,
    UnknownType,
)
from veridic.taxonomy import DEFAULT_CLASSIFICATION_REGISTRY as REGISTRY


def test_complete_classification_path():
    classification = REGISTRY.classify(
        "Temporal",
        "Measurement",
        "Duration",
    )

    assert classification.lineage() == (
        "Temporal",
        "Measurement",
        "Duration",
    )

    assert classification.path == "Temporal.Measurement.Duration"


def test_kind_is_category_qualified():
    assert REGISTRY.has_kind("Temporal", "Measurement")
    assert REGISTRY.has_kind("Quantitative", "Measurement")
    assert REGISTRY.has_kind("Physical", "Measurement")

    assert (
        REGISTRY.classify(
            "Temporal",
            "Measurement",
            "Duration",
        ).kind_path
        == "Temporal.Measurement"
    )

    assert (
        REGISTRY.classify(
            "Physical",
            "Measurement",
            "Temperature",
        ).kind_path
        == "Physical.Measurement"
    )


def test_type_requires_correct_kind_parent():
    with raises(UnknownType):
        REGISTRY.classify(
            "Temporal",
            "Coordinate",
            "Duration",
        )


def test_type_requires_correct_category_lineage():
    with raises(UnknownType):
        REGISTRY.classify(
            "Physical",
            "Measurement",
            "Duration",
        )


def test_kind_requires_correct_category_parent():
    with raises(UnknownKind):
        REGISTRY.classify(
            "Identity",
            "Measurement",
            "IPv4Address",
        )


def test_unknown_category_is_rejected():
    with raises(UnknownCategory):
        REGISTRY.classify(
            "Imaginary",
            "Measurement",
            "Duration",
        )


def test_cannot_register_kind_without_category():
    registry = ClassificationRegistry()

    with raises(UnknownCategory):
        registry.register_kind(
            "Temporal",
            "Coordinate",
        )


def test_cannot_register_type_without_kind():
    registry = ClassificationRegistry()
    registry.register_category("Temporal")

    with raises(UnknownKind):
        registry.register_type(
            "Temporal",
            "Coordinate",
            "Timestamp",
        )


def test_duplicate_category_is_rejected():
    registry = ClassificationRegistry()
    registry.register_category("Temporal")

    with raises(DuplicateClassification):
        registry.register_category("Temporal")


def test_direct_classification_is_structurally_valid_but_unregistered():
    classification = Classification(
        category="Temporal",
        kind="ImpossibleKind",
        type="ImpossibleType",
    )

    with raises(UnknownKind):
        REGISTRY.validate(classification)
