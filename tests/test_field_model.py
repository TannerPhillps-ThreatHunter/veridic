from veridic.catalog import DURATION, SOURCE_IPV4, TIMESTAMP_START
from veridic.utilities.units import SECOND
from veridic.vocabulary import Scale


def test_classification_is_tiered():
    assert TIMESTAMP_START.category == "Temporal"
    assert TIMESTAMP_START.kind == "Coordinate"
    assert TIMESTAMP_START.type == "Timestamp"


def test_measurement_is_not_part_of_classification_chain():
    assert DURATION.category == "Temporal"
    assert DURATION.kind == "Measurement"
    assert DURATION.type == "Duration"

    assert DURATION.scale is Scale.RATIO
    assert DURATION.unit_name == "second"


def test_role_is_contextual_semantics():
    assert SOURCE_IPV4.type == "IPv4Address"
    assert SOURCE_IPV4.role == "Participant.Source"


def test_field_signature_excludes_name_and_value():
    signature = DURATION.semantic_signature

    assert signature == (
        "Temporal",
        "Measurement",
        "Duration",
        Scale.RATIO,
        "Event.Duration",
        SECOND,
    )
