"""Semantic coherence contracts.

A Field classification carries claims about meaning.

A SemanticContract defines the independent Scale, Unit, and Dimension
properties that are coherent with that classification.

This allows Veridic to detect contradictions such as:

    Type:
        DataRate

    Dimension:
        Length / Time

or:

    Type:
        EmployeeIdentifier

    Unit:
        second

The classification and measurement systems remain independent, but
their conclusions must agree.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .field import Field
from .utilities.dimensions import (
    ANGLE,
    COUNT,
    DATA,
    LENGTH,
    TEMPERATURE,
    TIME,
    Dimension,
)
from .utilities.truth import Truth
from .vocabulary import Scale


class ContractError(ValueError):
    """Base semantic-contract error."""


class DuplicateContract(ContractError):
    """A contract already exists for the classification."""


class ContractViolation(ContractError):
    """A Field contradicts its registered semantic contract."""


class UnitPolicy(str, Enum):
    """Whether a classification permits a Unit."""

    REQUIRED = "required"
    OPTIONAL = "optional"
    FORBIDDEN = "forbidden"


@dataclass(frozen=True, slots=True)
class ContractEvaluation:
    """Result of comparing one Field to its semantic contract."""

    field: Field
    truth: Truth
    reasons: tuple[str, ...] = ()

    @property
    def coherent(self) -> bool:
        return self.truth is Truth.TRUE

    @property
    def contradictory(self) -> bool:
        return self.truth is Truth.FALSE

    @property
    def unknown(self) -> bool:
        return self.truth is Truth.UNKNOWN


@dataclass(frozen=True, slots=True)
class SemanticContract:
    """Expected semantic shape for one classification path."""

    classification_path: str
    allowed_scales: frozenset[Scale]
    dimension: Dimension | None = None
    unit_policy: UnitPolicy = UnitPolicy.OPTIONAL

    def evaluate(
        self,
        field: Field,
    ) -> ContractEvaluation:
        reasons: list[str] = []

        if (
            field.classification_path
            != self.classification_path
        ):
            reasons.append(
                "classification mismatch: "
                f"{field.classification_path} != "
                f"{self.classification_path}"
            )

        if field.scale not in self.allowed_scales:
            expected = ", ".join(
                sorted(
                    scale.value
                    for scale
                    in self.allowed_scales
                )
            )

            reasons.append(
                "invalid scale: "
                f"{field.scale.value}; "
                f"expected one of [{expected}]"
            )

        if (
            self.unit_policy
            is UnitPolicy.REQUIRED
            and field.unit is None
        ):
            reasons.append(
                "unit is required"
            )

        if (
            self.unit_policy
            is UnitPolicy.FORBIDDEN
            and field.unit is not None
        ):
            reasons.append(
                "unit is forbidden"
            )

        if (
            self.dimension is not None
            and field.unit is not None
            and field.dimension
            != self.dimension
        ):
            reasons.append(
                "dimension mismatch: "
                f"{field.dimension} != "
                f"{self.dimension}"
            )

        truth = (
            Truth.FALSE
            if reasons
            else Truth.TRUE
        )

        return ContractEvaluation(
            field=field,
            truth=truth,
            reasons=tuple(reasons),
        )


class ContractRegistry:
    """Classification-path semantic contracts."""

    def __init__(self) -> None:
        self._contracts: dict[
            str,
            SemanticContract,
        ] = {}

    def register(
        self,
        contract: SemanticContract,
    ) -> None:
        path = contract.classification_path

        if path in self._contracts:
            raise DuplicateContract(
                path
            )

        self._contracts[path] = contract

    def resolve(
        self,
        classification_path: str,
    ) -> SemanticContract | None:
        return self._contracts.get(
            classification_path
        )

    def evaluate(
        self,
        field: Field,
    ) -> ContractEvaluation:
        contract = self.resolve(
            field.classification_path
        )

        if contract is None:
            return ContractEvaluation(
                field=field,
                truth=Truth.UNKNOWN,
                reasons=(
                    "no semantic contract registered",
                ),
            )

        return contract.evaluate(
            field
        )

    def assert_coherent(
        self,
        field: Field,
    ) -> ContractEvaluation:
        evaluation = self.evaluate(
            field
        )

        if evaluation.contradictory:
            details = "; ".join(
                evaluation.reasons
            )

            raise ContractViolation(
                f"{field.classification_path}: "
                f"{details}"
            )

        return evaluation

    def contracts(
        self,
    ) -> tuple[SemanticContract, ...]:
        return tuple(
            self._contracts[
                path
            ]
            for path in sorted(
                self._contracts
            )
        )


def _contract(
    path: str,
    scales: set[Scale],
    *,
    dimension: Dimension | None = None,
    unit_policy: UnitPolicy = UnitPolicy.OPTIONAL,
) -> SemanticContract:
    return SemanticContract(
        classification_path=path,
        allowed_scales=frozenset(
            scales
        ),
        dimension=dimension,
        unit_policy=unit_policy,
    )


def build_default_contract_registry() -> ContractRegistry:
    registry = ContractRegistry()

    contracts = (
        _contract(
            "Temporal.Coordinate.Timestamp",
            {Scale.INTERVAL},
            dimension=TIME,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Temporal.Measurement.Duration",
            {Scale.RATIO},
            dimension=TIME,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Quantitative.Measurement.ByteCount",
            {Scale.RATIO},
            dimension=DATA,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Quantitative.Counter.PacketCount",
            {Scale.RATIO},
            dimension=COUNT,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Quantitative.Rate.DataRate",
            {Scale.RATIO},
            dimension=DATA / TIME,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Quantitative.Rate.PacketRate",
            {Scale.RATIO},
            dimension=COUNT / TIME,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Quantitative.Measurement.Scalar",
            {Scale.RATIO},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
        _contract(
            "Physical.Measurement.Temperature",
            {
                Scale.INTERVAL,
                Scale.RATIO,
            },
            dimension=TEMPERATURE,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Physical.Measurement.TemperatureDifference",
            {Scale.RATIO},
            dimension=TEMPERATURE,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Spatial.Coordinate.Latitude",
            {Scale.INTERVAL},
            dimension=ANGLE,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Spatial.Coordinate.ProjectedCoordinate",
            {Scale.INTERVAL},
            dimension=LENGTH,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Spatial.Measurement.Displacement",
            {Scale.RATIO},
            dimension=LENGTH,
            unit_policy=UnitPolicy.REQUIRED,
        ),
        _contract(
            "Identity.Address.IPv4Address",
            {Scale.NOMINAL},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
        _contract(
            "Identity.Address.IPv6Address",
            {Scale.NOMINAL},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
        _contract(
            "Identity.Address.MACAddress",
            {Scale.NOMINAL},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
        _contract(
            "Identity.Identifier.EmployeeIdentifier",
            {Scale.NOMINAL},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
        _contract(
            "Identity.Identifier.UUID",
            {Scale.NOMINAL},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
        _contract(
            "Categorical.Classification.Severity",
            {Scale.ORDINAL},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
        _contract(
            "Descriptive.Text.FreeText",
            {Scale.NOMINAL},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
        _contract(
            "Categorical.Collection.TagSet",
            {Scale.NOMINAL},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
        _contract(
            "Relational.Relationship.Edge",
            {Scale.NOMINAL},
            unit_policy=UnitPolicy.FORBIDDEN,
        ),
    )

    for contract in contracts:
        registry.register(
            contract
        )

    return registry


DEFAULT_CONTRACT_REGISTRY = (
    build_default_contract_registry()
)


__all__ = [
    "DEFAULT_CONTRACT_REGISTRY",
    "ContractError",
    "ContractEvaluation",
    "ContractRegistry",
    "ContractViolation",
    "DuplicateContract",
    "SemanticContract",
    "UnitPolicy",
    "build_default_contract_registry",
]
