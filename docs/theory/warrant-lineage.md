# Warrant Lineage

## Problem

Veridic now preserves every active Knowledge item supporting a
Proposition.

That creates a new danger:

    warrant multiplicity

may be mistaken for:

    independent corroboration

These are not equivalent.

---

# Example

Suppose:

    K1 = ASSERT P

Then:

    K2 = DERIVE P FROM K1

    K3 = DERIVE P FROM K1

    K4 = DERIVE P FROM K2

There are four Knowledge items warranting P.

But they do not constitute four independent epistemic origins.

All depend upon the original assertion K1.

Therefore:

    warrant count = 4

does not imply:

    independent support = 4

---

# Assertion Roots

Every Knowledge item has an assertion-root ancestry.

For an Assertion:

    roots(K1) = {K1}

For a Derivation:

    roots(Kd)
        =
    union(
        roots(each premise)
    )

Example:

    K1 = ASSERT A
    K2 = ASSERT B

    K3 = DERIVE P
         FROM K1, K2

Then:

    roots(K3)
        =
    {K1, K2}

Derivation does not manufacture new epistemic roots.

It transforms warranted information under a Law.

---

# Lineage Dependence

Two warrants are lineage-dependent when their assertion-root sets
overlap.

For:

    roots(KA) = {A, B}

and:

    roots(KB) = {B, C}

the shared root:

    B

means the warrants are not lineage-disjoint.

This relation is transitive when grouping warrants.

If:

    K1 overlaps K2

and:

    K2 overlaps K3

then all three belong to one lineage group.

---

# Lineage Groups

For a Proposition P, Veridic now distinguishes:

    warrant_count(P)

from:

    lineage_count(P)

Example:

    K1 = ASSERT P

    K2 = DERIVE P
         FROM K1, S

    K3 = DERIVE P
         FROM K1, S

Then:

    warrant_count(P) = 3

while:

    lineage_count(P) = 1

because all three support paths share assertion ancestry.

---

# Independent Derived Support

Suppose instead:

    K1 = ASSERT event.start

    K2 = ASSERT event.end

    K3 = DERIVE event.duration
         FROM K1, K2

and independently:

    K4 = ASSERT event.duration

If both K3 and K4 support the same Proposition:

    event.duration = 5 s

then their assertion roots are:

    roots(K3)
        =
    {K1, K2}

    roots(K4)
        =
    {K4}

The sets are disjoint.

Therefore they form two lineage groups.

This is stronger evidence than simply deriving the same result through
multiple branches from K1 and K2.

---

# Conservative Rule

Phase 13 uses a deliberately conservative rule:

    any shared assertion root
        ->
    shared lineage group

Even an apparently trivial shared premise such as an asserted constant
causes the lineages to be grouped.

This prevents Veridic from overstating independence.

Later work may distinguish epistemically material premises from
semantically auxiliary premises.

No such distinction is introduced yet.

---

# What This Does Not Prove

Lineage-disjointness is not full epistemic independence.

Two different Assertion roots may still come from:

    the same sensor

    the same observer

    the same upstream dataset

    the same collection system

    the same model

    the same causal event

    duplicated source material

Therefore:

    lineage independence
        !=
    source independence

and:

    source independence
        !=
    causal independence

Phase 13 solves only the first structural problem.

---

# Support Stack

The current epistemic model becomes:

    Proposition
        |
        v
    Knowledge
        |
        +-- Warrant
        +-- State
        |
        v
    Support
        |
        +-- FOR
        +-- AGAINST
        |
        v
    Warrant Lineage
        |
        +-- assertion roots
        +-- lineage groups

Thus Veridic can answer separately:

    How many warrants support P?

and:

    How many assertion-lineage groups support P?

These numbers need not be equal.

---

# Current Finding

The appropriate distinction is:

    Warrant Multiplicity
        !=
    Lineage Independence

A Derivation increases warranted Knowledge.

It does not automatically increase epistemic independence.

That property must be established from lineage.
