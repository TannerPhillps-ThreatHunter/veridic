"""Experimental Field classification taxonomy.

This registry exists for testing the Category -> Kind -> Type model.
Its contents are provisional.
"""

from __future__ import annotations

from .hierarchy import ClassificationRegistry


def build_default_registry() -> ClassificationRegistry:
    registry = ClassificationRegistry()

    # --------------------------------------------------------
    # Categories
    # --------------------------------------------------------

    for category in (
        "Categorical",
        "Descriptive",
        "Identity",
        "Physical",
        "Quantitative",
        "Relational",
        "Spatial",
        "Temporal",
    ):
        registry.register_category(category)

    # --------------------------------------------------------
    # Identity
    # --------------------------------------------------------

    registry.register_kind("Identity", "Address")
    registry.register_kind("Identity", "Identifier")
    registry.register_kind("Identity", "Name")
    registry.register_kind("Identity", "Reference")

    registry.register_type("Identity", "Address", "IPv4Address")
    registry.register_type("Identity", "Address", "IPv6Address")
    registry.register_type("Identity", "Address", "MACAddress")

    registry.register_type(
        "Identity",
        "Identifier",
        "EmployeeIdentifier",
    )
    registry.register_type("Identity", "Identifier", "UUID")

    registry.register_type("Identity", "Name", "HumanName")
    registry.register_type("Identity", "Reference", "URI")

    # --------------------------------------------------------
    # Temporal
    # --------------------------------------------------------

    registry.register_kind("Temporal", "Coordinate")
    registry.register_kind("Temporal", "Interval")
    registry.register_kind("Temporal", "Measurement")

    registry.register_type("Temporal", "Coordinate", "Timestamp")
    registry.register_type("Temporal", "Coordinate", "Date")
    registry.register_type("Temporal", "Coordinate", "TimeOfDay")

    registry.register_type("Temporal", "Interval", "TimeInterval")

    registry.register_type("Temporal", "Measurement", "Duration")

    # --------------------------------------------------------
    # Quantitative
    # --------------------------------------------------------

    registry.register_kind("Quantitative", "Counter")
    registry.register_kind("Quantitative", "Measurement")
    registry.register_kind("Quantitative", "Rate")

    registry.register_type(
        "Quantitative",
        "Counter",
        "PacketCount",
    )

    registry.register_type(
        "Quantitative",
        "Measurement",
        "ByteCount",
    )

    registry.register_type(
        "Quantitative",
        "Rate",
        "DataRate",
    )
    registry.register_type(
        "Quantitative",
        "Rate",
        "PacketRate",
    )

    # --------------------------------------------------------
    # Categorical
    # --------------------------------------------------------

    registry.register_kind("Categorical", "Classification")
    registry.register_kind("Categorical", "Collection")
    registry.register_kind("Categorical", "Label")

    registry.register_type(
        "Categorical",
        "Classification",
        "Severity",
    )
    registry.register_type(
        "Categorical",
        "Collection",
        "TagSet",
    )
    registry.register_type(
        "Categorical",
        "Label",
        "CategoryLabel",
    )

    # --------------------------------------------------------
    # Spatial
    # --------------------------------------------------------

    registry.register_kind("Spatial", "Coordinate")
    registry.register_kind("Spatial", "Measurement")

    registry.register_type(
        "Spatial",
        "Coordinate",
        "Latitude",
    )
    registry.register_type(
        "Spatial",
        "Coordinate",
        "Longitude",
    )
    registry.register_type(
        "Spatial",
        "Measurement",
        "Distance",
    )

    # --------------------------------------------------------
    # Physical
    # --------------------------------------------------------

    registry.register_kind("Physical", "Measurement")

    registry.register_type(
        "Physical",
        "Measurement",
        "Temperature",
    )
    registry.register_type(
        "Physical",
        "Measurement",
        "Mass",
    )

    # --------------------------------------------------------
    # Descriptive
    # --------------------------------------------------------

    registry.register_kind("Descriptive", "Text")

    registry.register_type(
        "Descriptive",
        "Text",
        "FreeText",
    )

    # --------------------------------------------------------
    # Relational
    # --------------------------------------------------------

    registry.register_kind("Relational", "Relationship")

    registry.register_type(
        "Relational",
        "Relationship",
        "Edge",
    )

    return registry


DEFAULT_CLASSIFICATION_REGISTRY = build_default_registry()
