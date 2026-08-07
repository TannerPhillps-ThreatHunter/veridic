from veridic.dimensions import SemanticDimension as D
from veridic.domain_laws import DOMAIN_LAWS


def _laws_using(dimension: D) -> set[str]:
    return {
        law.name
        for law in DOMAIN_LAWS
        if dimension in law.depends_on
    }


def test_category_is_used_by_real_domain_laws():
    assert _laws_using(D.CATEGORY)


def test_kind_is_used_by_real_domain_laws():
    assert _laws_using(D.KIND)


def test_type_is_used_by_real_domain_laws():
    assert _laws_using(D.TYPE)


def test_scale_is_used_by_real_domain_laws():
    assert _laws_using(D.SCALE)


def test_unit_is_used_by_real_domain_laws():
    assert _laws_using(D.UNIT)


def test_role_has_independent_real_domain_use():
    laws = _laws_using(D.ROLE)

    assert "domain-projected-coordinate-difference" in laws


def test_value_not_required_for_static_operation_admission_yet():
    assert not _laws_using(D.VALUE)


def test_invariants_not_required_for_static_admission_yet():
    assert not _laws_using(D.INVARIANTS)
