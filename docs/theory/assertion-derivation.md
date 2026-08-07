# Assertion Over, Derivation Under

## Research Question

Are Assertion and Derivation sufficient as the two root computational
acts of Veridic?

The current implementation narrows this question.

The stronger defensible formulation is:

> Are Assertion and Derivation sufficient as the two root
> knowledge-producing acts of Veridic?

Phase 10 tests that hypothesis.

---

# Assertion

Assertion introduces knowledge into the current Veridic computational
world.

Examples include:

    external input
    observation
    measurement
    imported data
    nondeterministic boundary input

These cases differ in provenance, but each has the same computational
shape:

    externally supplied knowledge
        ->
    semantically typed value

Therefore they do not currently require distinct root computational
acts.

Their differences are represented through Provenance.

---

# Derivation

Derivation establishes new knowledge from existing knowledge through an
admitted Operation.

Example:

    ASSERT event.start = 10 s
    ASSERT event.end   = 15 s

    DERIVE event.duration =
        event.end - event.start

The result retains:

    operation
    operands
    semantic rule
    governing laws

Therefore the value remains explainable.

---

# KnownValue

FieldValue continues to answer:

    What is this value?

KnownValue answers:

    What is this value?

and:

    How does Veridic know it?

Therefore epistemic origin remains layered above Field semantics rather
than being inserted into the Field classification hierarchy.

---

# Dependency Graph

A Derivation explicitly records its operand knowledge identifiers.

This produces a dependency graph naturally:

    event.start ----\
                     -> event.duration
    event.end ------/         |
                               v
    network.bytes -------> network.rate

This permits transitive dependency discovery.

---

# Invalidation

When an Assertion changes, existing Derivations that depended upon the
previous Assertion are no longer justified.

They become:

    INVALID

They do not silently retain epistemic validity.

Example:

    event.end = 15 s

changes to:

    event.end = 20 s

Then:

    event.duration
    network.rate

are invalidated.

Recomputation is intentionally not automatic yet.

Invalidation must be correct before reactive recomputation is added.

---

# Retraction

Retraction does not create knowledge.

It changes the lifecycle state of existing knowledge.

Therefore current evidence does not justify Retraction as a third
knowledge-producing primitive.

The distinction is:

    origin:
        Assertion | Derivation

    state:
        Active | Invalid | Retracted

These answer different questions.

---

# Failed Derivation

A failed Derivation produces no KnownValue.

For example:

    IPv4Address + IPv4Address

fails semantic admission.

No derived knowledge node is created.

Failure is therefore an execution outcome, not a third epistemic origin.

---

# Observation

Observation currently reduces to:

    Assertion
        +
    Provenance(method="observation")

No information is lost by this reduction in the current model.

---

# Measurement

Measurement currently reduces to:

    Assertion
        +
    quantitative Field semantics
        +
    Unit
        +
    Provenance(method="measurement")

If a future measurement is computed from lower-level sensor evidence,
that result may instead be a Derivation.

The epistemic distinction depends on how the value entered the current
computational world, not merely on the word "measurement."

---

# Nondeterminism

A value obtained from an external nondeterministic source remains an
Assertion at the system boundary.

Its unpredictability does not make it a third form of knowledge origin.

Its Provenance records the nondeterministic source.

---

# Competing Knowledge

Multiple Assertions or Derivations may eventually disagree.

Contradiction is not itself a knowledge-producing act.

It is a relation between knowledge claims.

Conflict semantics remain a future research problem.

---

# Recursive Derivation

The current KnowledgeStore constructs Derivations only from knowledge
nodes that already exist.

A new node cannot depend on itself before it exists.

Therefore the current graph is acyclic by construction.

Recursive semantic systems may eventually require an explicit fixed-point
model.

That should not be added until a concrete domain requires it.

---

# External Action and Side Effects

Actions that change the external world do not reduce naturally to either
Assertion or Derivation.

However, they also do not produce knowledge merely by occurring.

This suggests a boundary:

    Epistemic computation:
        Assertion
        Derivation

    Agency / world mutation:
        Action

Therefore the existence of external side effects does not currently
falsify the two-act epistemic hypothesis.

It may demonstrate that Assertion and Derivation are not the only root
acts of the entire future Veridic language.

---

# Current Finding

Current adversarial cases support:

    Assertion
        knowledge introduced

    Derivation
        knowledge established

as sufficient root acts for knowledge production.

They do not yet support the stronger claim that all computation reduces
to Assertion or Derivation.

That stronger claim remains unproven.

---

# Working Principle

Every KnownValue must have an explicit epistemic origin.

A value is either:

    asserted

or:

    derived

A derived value must retain sufficient lineage to justify its existence.

This remains a working principle until broader computational testing
supports promotion to a Veridic law.
