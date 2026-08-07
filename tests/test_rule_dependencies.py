from veridic.dimensions import SemanticDimension as D
from veridic.rules import build_runtime
from veridic.tier_experiments import build_tier_experiment_runtime
from veridic.vocabulary import Operation


def test_timestamp_subtraction_declares_classification_dependencies():
    runtime = build_runtime()

    rules = [
        rule
        for rule in runtime.rules
        if rule.name == "temporal-coordinate-difference"
    ]

    assert len(rules) == 1

    rule = rules[0]

    assert rule.depends_on_dimension(D.CATEGORY)
    assert rule.depends_on_dimension(D.KIND)
    assert rule.depends_on_dimension(D.TYPE)
    assert rule.depends_on_dimension(D.SCALE)
    assert rule.depends_on_dimension(D.UNIT)


def test_experiment_runtime_uses_category_sensitive_rules():
    runtime = build_tier_experiment_runtime()

    sub_rules = [
        rule
        for rule in runtime.rules
        if rule.operation is Operation.SUB
    ]

    assert sub_rules

    assert all(
        rule.depends_on_dimension(D.CATEGORY)
        for rule in sub_rules
    )


def test_equality_rule_declares_type_dependency():
    runtime = build_tier_experiment_runtime()

    rules = [
        rule
        for rule in runtime.rules
        if rule.operation is Operation.EQ
    ]

    assert len(rules) == 1
    assert rules[0].depends_on_dimension(D.TYPE)
