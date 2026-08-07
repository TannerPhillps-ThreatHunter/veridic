from fieldframe.relations import Relation, supports
from fieldframe.vocabulary import Scale


def test_nominal_supports_equality_only():
    assert supports(Scale.NOMINAL, Relation.EQUALITY)
    assert not supports(Scale.NOMINAL, Relation.ORDER)
    assert not supports(Scale.NOMINAL, Relation.DIFFERENCE)
    assert not supports(Scale.NOMINAL, Relation.RATIO)


def test_ordinal_adds_order():
    assert supports(Scale.ORDINAL, Relation.EQUALITY)
    assert supports(Scale.ORDINAL, Relation.ORDER)
    assert not supports(Scale.ORDINAL, Relation.DIFFERENCE)


def test_interval_adds_difference():
    assert supports(Scale.INTERVAL, Relation.DIFFERENCE)
    assert not supports(Scale.INTERVAL, Relation.RATIO)


def test_ratio_adds_ratio_relation():
    assert supports(Scale.RATIO, Relation.RATIO)
