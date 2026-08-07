from veridic.catalog import (
    BYTE_COUNT,
    DURATION,
    EDGE,
    FREE_TEXT,
    LATITUDE,
    SOURCE_IPV4,
    TAG_SET,
    TEMPERATURE,
    TIMESTAMP_START,
)


def test_temporal_coordinate():
    assert TIMESTAMP_START.classification_path == (
        "Temporal.Coordinate.Timestamp"
    )


def test_temporal_measurement():
    assert DURATION.classification_path == (
        "Temporal.Measurement.Duration"
    )


def test_identity_address():
    assert SOURCE_IPV4.classification_path == (
        "Identity.Address.IPv4Address"
    )


def test_quantitative_measurement():
    assert BYTE_COUNT.classification_path == (
        "Quantitative.Measurement.ByteCount"
    )


def test_physical_measurement():
    assert TEMPERATURE.classification_path == (
        "Physical.Measurement.Temperature"
    )


def test_spatial_coordinate():
    assert LATITUDE.classification_path == (
        "Spatial.Coordinate.Latitude"
    )


def test_descriptive_text():
    assert FREE_TEXT.classification_path == (
        "Descriptive.Text.FreeText"
    )


def test_categorical_collection():
    assert TAG_SET.classification_path == (
        "Categorical.Collection.TagSet"
    )


def test_relational_relationship():
    assert EDGE.classification_path == (
        "Relational.Relationship.Edge"
    )
