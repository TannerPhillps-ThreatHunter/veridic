"""Tiered Field classification hierarchy.

The classification layer has exactly three semantic tiers:

    Category -> Kind -> Type

Each lower tier exists only within the lineage established by its parent.

Examples:

    Temporal -> Coordinate -> Timestamp
    Temporal -> Measurement -> Duration
    Identity -> Address -> IPv4Address
    Quantitative -> Counter -> PacketCount

The hierarchy is intentionally open-vocabulary. Category, Kind, and Type
names are semantic identifiers rather than closed Python enums.
"""

from __future__ import annotations

from dataclasses import dataclass


class ClassificationError(ValueError):
    """Base error for invalid Field classification."""


class UnknownCategory(ClassificationError):
    """A Category has not been registered."""


class UnknownKind(ClassificationError):
    """A Kind has not been registered beneath the requested Category."""


class UnknownType(ClassificationError):
    """A Type has not been registered beneath the requested Kind."""


class DuplicateClassification(ClassificationError):
    """A hierarchy member was registered more than once."""


@dataclass(frozen=True, slots=True)
class Classification:
    """A complete Category -> Kind -> Type classification path."""

    category: str
    kind: str
    type: str

    def __post_init__(self) -> None:
        for name, value in (
            ("category", self.category),
            ("kind", self.kind),
            ("type", self.type),
        ):
            if not value or not value.strip():
                raise ClassificationError(f"{name} must be non-empty")

    @property
    def path(self) -> str:
        """Fully qualified semantic classification."""

        return f"{self.category}.{self.kind}.{self.type}"

    @property
    def kind_path(self) -> str:
        """Category-qualified Kind identifier."""

        return f"{self.category}.{self.kind}"

    def lineage(self) -> tuple[str, str, str]:
        """Return the ordered tier lineage."""

        return self.category, self.kind, self.type


class ClassificationRegistry:
    """Registry enforcing the three-tier Field classification hierarchy.

    The registry deliberately keys Kind by:

        (Category, Kind)

    and Type by:

        (Category, Kind, Type)

    This means:

        Temporal.Measurement

    and:

        Physical.Measurement

    are distinct semantic Kinds even though they share a label.
    """

    def __init__(self) -> None:
        self._categories: set[str] = set()
        self._kinds: set[tuple[str, str]] = set()
        self._types: set[tuple[str, str, str]] = set()

    def register_category(self, category: str) -> None:
        category = self._normalize(category)

        if category in self._categories:
            raise DuplicateClassification(
                f"Category already registered: {category}"
            )

        self._categories.add(category)

    def register_kind(self, category: str, kind: str) -> None:
        category = self._normalize(category)
        kind = self._normalize(kind)

        if category not in self._categories:
            raise UnknownCategory(
                f"Cannot register Kind {kind!r}: "
                f"unknown Category {category!r}"
            )

        key = (category, kind)

        if key in self._kinds:
            raise DuplicateClassification(
                f"Kind already registered: {category}.{kind}"
            )

        self._kinds.add(key)

    def register_type(
        self,
        category: str,
        kind: str,
        type_name: str,
    ) -> None:
        category = self._normalize(category)
        kind = self._normalize(kind)
        type_name = self._normalize(type_name)

        if category not in self._categories:
            raise UnknownCategory(
                f"Cannot register Type {type_name!r}: "
                f"unknown Category {category!r}"
            )

        if (category, kind) not in self._kinds:
            raise UnknownKind(
                f"Cannot register Type {type_name!r}: "
                f"unknown Kind {category}.{kind}"
            )

        key = (category, kind, type_name)

        if key in self._types:
            raise DuplicateClassification(
                "Type already registered: "
                f"{category}.{kind}.{type_name}"
            )

        self._types.add(key)

    def validate(self, classification: Classification) -> None:
        """Require an exact registered Category -> Kind -> Type path."""

        category, kind, type_name = classification.lineage()

        if category not in self._categories:
            raise UnknownCategory(
                f"Unknown Category: {category}"
            )

        if (category, kind) not in self._kinds:
            raise UnknownKind(
                f"Unknown Kind lineage: {category}.{kind}"
            )

        if (category, kind, type_name) not in self._types:
            raise UnknownType(
                "Unknown Type lineage: "
                f"{category}.{kind}.{type_name}"
            )

    def classify(
        self,
        category: str,
        kind: str,
        type_name: str,
    ) -> Classification:
        """Construct and validate a Classification."""

        classification = Classification(
            category=self._normalize(category),
            kind=self._normalize(kind),
            type=self._normalize(type_name),
        )

        self.validate(classification)

        return classification

    def has_category(self, category: str) -> bool:
        return self._normalize(category) in self._categories

    def has_kind(self, category: str, kind: str) -> bool:
        return (
            self._normalize(category),
            self._normalize(kind),
        ) in self._kinds

    def has_type(
        self,
        category: str,
        kind: str,
        type_name: str,
    ) -> bool:
        return (
            self._normalize(category),
            self._normalize(kind),
            self._normalize(type_name),
        ) in self._types

    def categories(self) -> tuple[str, ...]:
        return tuple(sorted(self._categories))

    def kinds(self) -> tuple[tuple[str, str], ...]:
        return tuple(sorted(self._kinds))

    def types(self) -> tuple[tuple[str, str, str], ...]:
        return tuple(sorted(self._types))

    @staticmethod
    def _normalize(value: str) -> str:
        value = value.strip()

        if not value:
            raise ClassificationError(
                "Classification identifiers must be non-empty"
            )

        return value
