from fieldframe.catalog import EMPLOYEE_ID
from fieldframe.dataframe import SemanticDataFrame


def test_integer_representation_does_not_make_identifier_quantitative():
    frame = SemanticDataFrame.from_data(
        {
            "employee.id": [
                1001,
                1002,
                1003,
            ],
        },
        {
            "employee.id": EMPLOYEE_ID,
        },
    )

    physical = frame.to_polars()

    assert physical[
        "employee.id"
    ].dtype.is_integer()

    semantic = frame.field(
        "employee.id"
    )

    assert (
        semantic.classification_path
        == (
            "Identity.Identifier."
            "EmployeeIdentifier"
        )
    )

    assert semantic.scale.value == "nominal"
