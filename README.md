# Veridic

**A field-aware semantic DataFrame runtime.**

Veridic is a research and engineering project exploring a layered and
tiered model of data fields and the computational consequences of making
field semantics explicit.

The working Field model considers:

- Field Category
- Field Kind
- Field Type
- Field Scale
- Field Value
- Field Role
- Field Unit
- Field Invariants

The central research hypothesis is that DataFrame operations should operate
over both values and their field semantics.

A Veridic operation should be able to determine:

1. whether an operation is representationally executable;
2. whether the operation is semantically meaningful;
3. what Field semantics the result acquires; and
4. whether contextual invariants remain satisfied.

The initial computational model is:

    Admit -> Execute -> Transfer -> Verify

Veridic is currently experimental research. The field hierarchy,
operation algebra, and runtime semantics are not yet considered stable.

## Current Runtime

Veridic now includes an experimental `SemanticDataFrame` backed by
Polars.

```text
SemanticDataFrame
    |
    +-- SemanticSchema
    |       |
    |       +-- Field
    |
    +-- SemanticRuntime
    |
    +-- Invariant Validation
    |
    +-- Polars```
A derived column transforms both semantics and values:

FieldA x FieldB -> FieldOut
ValueA x ValueB -> ValueOut

Veridic distinguishes:

Representational Validity
    ->
Semantic Validity
    ->
Contextual Validity

See docs/theory/semantic-dataframe.md.

## Native Dimensions and Units

Veridic implements its own dependency-free dimensional and unit algebra.

```text
Dimension
    |
    +-- Time
    +-- Length
    +-- Mass
    +-- Temperature
    +-- Data
    +-- Count
    +-- Angle

Unit
    |
    +-- Dimension
    +-- Scale
    +-- Offset```
Compound units are derived algebraically:

byte / second
    ->
Data / Time

Affine units such as absolute Celsius are explicitly distinguished from
linear difference units.

## Semantic Coherence

Veridic independently derives and cross-checks semantic properties.

```text
Field Algebra
    ->
Type

Unit Algebra
    ->
Unit

Dimension Algebra
    ->
Dimension

Measurement Semantics
    ->
Scale

        |
        v

Semantic Contract

        |
        v

TRUE | FALSE | UNKNOWN```
A Field claiming DataRate with dimension Length / Time is rejected
even if its underlying values are numerically computable.

## Assertion and Derivation

Veridic distinguishes knowledge introduced into a computation from
knowledge established by computation.

```text
Assertion
    |
    v
KnownValue
    |
    v
Semantic Operation
    |
    v
Derivation```
An asserted and derived value may have identical Field semantics and
datum while remaining epistemically distinct.

Derived values retain their dependencies and governing semantic rule,
allowing Veridic to explain why they exist and invalidate them when
their premises change.

## Data -> Information -> Knowledge

Veridic now distinguishes three semantic layers:

```text
Data
    |
    v
Information
    |
    +-- Assertion
    |
    +-- Derivation
    |
    v
Knowledge```
More precisely:

Knowledge = Information + Warrant

Warrant = Assertion | Derivation

A Proposition may exist without being accepted as Knowledge, and the
same Proposition may possess multiple independent warrants.

## Truth and Epistemic Support

Veridic does not treat contradictory warrants as a fourth truth value.

```text
Truth
    TRUE
    FALSE
    UNKNOWN

Support
    NEITHER
    FOR
    AGAINST
    BOTH```
BOTH means that active warranted Knowledge exists for both a
Proposition and its negation. It represents epistemic contest, not a
declaration that the Proposition is objectively both true and false.

## Warrant Lineage

Veridic distinguishes the number of warrants from the number of
assertion-lineage groups supporting a Proposition.

```text
K1 = ASSERT P
K2 = DERIVE P FROM K1
K3 = DERIVE P FROM K1

warrant count  = 3
lineage count  = 1```
Derivation can create additional warranted Knowledge without creating a
new epistemic root.

Lineage independence is intentionally narrower than source or causal
independence.

## Representation, Warrant, and Truth

Veridic distinguishes three independent questions:

```text
represented(P)?
warranted(P)?
true(P under Interpretation)?```
Worked for 1m 1s

The cross-model reduction finds three genuine redundancies and two semantic collisions. I would not add another model yet.

Phase 13 is canonical at 88cbe4c.

1. The foundational architecture survives

The strongest reduction remains:

Data→Information
Assertion∨Derivation
	​

Knowledge
	​


These three transitions correspond to genuinely different questions:

Model	Question	Candidate core
Data	What is represented?	Identity, Datum, Domain, Relation
Information	What is stated?	Proposition
Knowledge	Why may the statement be held?	Warrant = Assertion | Derivation

Everything after Knowledge currently looks derived:

Support
Lineage
Conflict
Corroboration

These should be treated as analyses over Knowledge, not additional foundational layers.

So I am retracting the loose formulation:

Data→Information→Knowledge→Support→Lineage

in favor of:

FOUNDATION

Data
  ↓
Information
  ↓
Knowledge


DERIVED ANALYSES OF KNOWLEDGE

Support
Lineage
Conflict
Corroboration
...
2. Collision: Information presence is currently being treated as Truth

This is the most important finding.

InformationState.evaluate() currently behaves essentially as:

P∈I⇒Truth(P)=TRUE
¬P∈I⇒Truth(P)=FALSE

and:

P,¬P∈I⇒InformationConflict

That is implemented directly in information.py.

But Phase 12 established:

Representation

=Truth
	​


and:

Support

=Truth
	​


If Veridic merely contains the proposition:

MALICIOUS(host:A)

that means:

Veridic represents the information that host A is malicious.

It does not mean:

host A is malicious is true.

That distinction was the whole reason we created Warrant.

So this:

InformationState.evaluate(P)

is theoretically wrong as currently named and interpreted.

Correct reduction

An Information State should answer:

Represented(I,P)?
	​


not:

True(P)?
	​


We actually have three different predicates:

Represented(P)
Warranted(P)
True(P)

Those cannot collapse.

3. Truth requires an interpretation

This leads to a deeper correction.

A Proposition is truth-apt, but it does not carry its truth value intrinsically.

Formally, truth is closer to:

Truth(P,M)
	​


where M is some interpretation/model/world against which P is evaluated.

For example:

P = HAS_VALUE(event.duration, 5s)

The Proposition exists independently of whether it is:

true
false
unknown

Therefore our semantic architecture should be:

Proposition
    truth-apt content

Representation
    whether Veridic contains P

Warrant
    why Veridic epistemically holds P

Truth Evaluation
    whether P obtains under an interpretation

That is much cleaner.

4. Redundancy: SemanticValue duplicates Field semantics

The current Information implementation contains:

SemanticValue {
    classification_path
    scale
    unit
    datum
}

while Field already contains classification, scale, unit, role, and invariants.

Then:

HAS_VALUE(
    Field,
    SemanticValue
)

means both sides contain overlapping semantic information.

This gave us useful verification redundancy in Phase 11, but as a foundational model it is suspicious.

We're encoding:

Field:
    Duration
    Ratio
    seconds

SemanticValue:
    Duration
    Ratio
    seconds
    5

twice.

The deeper Data reduction already suggested the cleaner form:

Value=⟨Domain,Datum⟩
	​


Then:

HAS_VALUE(Field,Value)

and semantic validity asks whether:

Domain(Value)

is admissible for:

ExpectedDomain(Field)

That gives us verification without semantic duplication.

So SemanticValue looks increasingly like a transitional executable adapter, not a primitive.

I would not delete it yet. But its theoretical status should be demoted.

5. Redundancy: InformationRelation is probably the executable face of Data Relation

Our Data Model says:

Relation

is a candidate primitive.

Then Information currently introduces:

InformationRelation

and an atomic Proposition:

AtomicProposition {
    relation
    terms
}

This is likely not two different concepts.

More probably:

Relation
	​


is the relational semantic definition, while:

Proposition=Relation(Terms)
	​


is its grounded application.

Exactly analogous to:

f

versus:

f(x)

So eventually:

InformationRelation

should probably reduce to:

Relation

from the Data foundation.

No new Information-level relation type is theoretically required.

6. Support survives, but only as a projection

Phase 12 implemented:

EpistemicSupport {
    proposition
    for_knowledge
    against_knowledge
}

with:

NEITHER
FOR
AGAINST
BOTH

The implementation itself explicitly describes these as epistemic support states rather than Truth.

This survives reduction nicely because:

Support(P,K)

is completely derivable from Knowledge.

Specifically:

Support
+
(P)={K
i
	​

∣proposition(K
i
	​

)=P}

and:

Support
−
(P)={K
i
	​

∣proposition(K
i
	​

)=¬P}

Therefore:

Support is not stored epistemic substance
	​


It is a query/projection over Knowledge.

That's good.

SupportState should remain derived.

7. Lineage also survives only as analysis

Phase 13 gives us:

roots(A)={A}

for Assertions, and:

roots(D)=⋃roots(premises(D))

for Derivations.

This does not introduce new epistemic content.

It reveals structure already present in Derivation warrants.

Therefore:

Lineage=Analysis(KnowledgeGraph)
	​


not:

Knowledge+Lineage

This is a very satisfying reduction.

We don't need to store lineage as another fundamental layer.

We can calculate it.

8. Collision: INVALID is carrying two meanings

This one is subtler.

Our Knowledge lifecycle currently has roughly:

ACTIVE
INVALID
RETRACTED

and changing a premise causes dependent derivations to become INVALID.

But consider:

T1:
    ASSERT end = 15
    DERIVE duration = 5

Later:

T2:
    ASSERT end = 20

Was the old derivation:

duration = 5

invalid?

Not necessarily.

It may have been perfectly valid relative to:

end = 15

It is simply no longer current relative to the new information state.

That suggests:

Invalidity

=Staleness
	​


A derivation can be:

semantically valid
epistemically justified from its premises
historically valid
but no longer current

So INVALID currently risks conflating:

Invalid

The warrant itself is defective.

with:

Stale

The warrant was valid but depends on premises that are no longer current.

This distinction has actual computational force, especially if Veridic becomes reactive or temporal.

We should investigate it before building more provenance machinery.

9. Collision: mutation destroys epistemic history

Our Knowledge stores currently modify lifecycle state by replacing the stored object.

Conceptually:

K1 active

becomes:

K1 invalid

or:

K1 retracted

But if Veridic is serious about lineage and provenance, we eventually need to answer:

Was K1 active at T1?
Why was it retracted?
What superseded it?
Which derivations were justified when K1 was current?

Mutating a status in place makes this harder.

The deeper model probably needs:

Knowledge Identity

to remain stable while lifecycle transitions are separately represented.

Possibly:

StateOf(K1, ACTIVE, T1)
StateOf(K1, RETRACTED, T2)

or event-like transitions.

But I would not implement that yet.

It first needs reduction against Identity, Relation, and temporal semantics.

10. Cross-model reduction

We can now simplify the conceptual architecture substantially.

Fundamental Data Model

Candidate:

Identity
	​

Datum
	​

Domain
	​

Relation
	​


Derived:

Value
Field
Binding
Context
Record
Event
Table
Graph
...
Fundamental Information Model

Only:

Proposition
	​


where:

Proposition=Relation(Terms)
	​


Derived:

Negation
Conjunction
Disjunction
Description
Record-description
Information set
...
Fundamental Knowledge Model

We need:

Knowledge
	​


as:

Knowledge=⟨Proposition,Warrant⟩
	​


with:

Warrant::=Assertion∣Derivation
	​


That's it so far.

11. Everything else moves out of the foundational spine
Truth

Evaluation of Proposition under an interpretation:

Truth(P,M)
State

Lifecycle of Knowledge:

State(K,t)
Support

Projection over active Knowledge:

Support(P,K)
Lineage

Graph analysis over warrants:

Lineage(K)
Provenance

Currently part of Assertion warrant, but not yet reduced.

Corroboration

Future analysis over support + lineage + provenance.

None of these currently justify becoming new foundational models.

12. The reduced Veridic architecture

This is now much smaller:

                VERIDIC

                 DATA
      ┌──────────┼───────────┐
   Identity    Datum       Domain
                 │
              Relation
                 │
                 ▼
             INFORMATION
                 │
            Proposition
                 │
        ┌────────┴────────┐
        │                 │
    Assertion         Derivation
        │                 │
        └────────┬────────┘
                 ▼
             KNOWLEDGE

Then outside the spine:

             KNOWLEDGE
                 │
       ┌─────────┼─────────┐
       │         │         │
     State    Support    Lineage
                 │
             Provenance
                 │
           Corroboration?

And independently:

Proposition
    │
    ▼
Interpretation
    │
    ▼
Truth

That last separation is particularly important.

13. One deeper insight

We have been speaking of:

Data→Information→Knowledge

as if each step transforms one object into another.

That is not quite right.

A better interpretation is progressive semantic commitment.

The Datum doesn't disappear when it becomes a Value.

The Value doesn't disappear when it participates in a Proposition.

The Proposition doesn't disappear when it becomes warranted Knowledge.

Instead:

Datum

is referenced by:

Value

which participates in:

Proposition

which participates in:

Knowledge

So the architecture is compositional:

Datum⊂Value⊂Proposition⊂Knowledge
	​


conceptually—not necessarily structurally as literal containment.

Each layer adds a new answer:

Datum
    What was represented?

Value
    What does it mean?

Proposition
    What is being said?

Knowledge
    Why may we hold it?

That is cleaner than thinking of information as transformed data and knowledge as transformed information.

Current verdict

After reduction, I would retain only three foundational models:

Data
	​

Information
	​

Knowledge
	​


and only the following current primitive candidates:

Data:Identity, Datum, Domain, Relation
	​

Information:Proposition
	​

Knowledge:Assertion, Derivation
	​


with Knowledge itself as their warranted composition.

Everything else has either reduced or remains unproven.

The next investigation should not be provenance yet. The cross-model audit found a more fundamental inconsistency first:

Veridic currently lacks a clean distinction between representation, epistemic warrant, and truth evaluation in executable semantics.

I would address that conceptual defect next—specifically determining what Truth actually means in Veridic and whether InformationState.evaluate() should survive at all—before we build anything further.

update, then Optimize, Then Refine, then upgrade and evolve
Worked for 1m 23s

Agreed. I’m applying those five verbs as an evolution discipline, not as permission to add five layers.

The repository shows exactly what needs correction: InformationState still infers Truth.TRUE/FALSE from represented propositions, while Truth itself is described as “epistemic truth.” Phase 12 has made both assumptions obsolete.

Update → Optimize → Refine → Upgrade → Evolve
Update

Correct:

Represented(P)

⇒True(P)
Optimize

Remove truth evaluation and InformationConflict from InformationState. Information should only record propositions.

Refine

Define three independent questions:

Represented(P)?
Warranted(P)?
True(P∣M)?
Upgrade

Introduce an explicit Interpretation boundary for Truth evaluation.

Evolve

Make the executable architecture match the reduced theory:

Data→Information
Warrant
	​

Knowledge
	​


while Truth is orthogonal:

Proposition+Interpretation→Truth
	​

Phase 14 — Representation ≠ Warrant ≠ Truth

Run this from the repository root:

set -eo pipefail

source .venv/bin/activate
export PYTHONPATH="$PWD/src"

echo
echo "=== Phase 14: representation, warrant, truth ==="

python - <<'PY'
from pathlib import Path

path = Path("src/veridic/information.py")
text = path.read_text()

text = text.replace(
    "from .utilities.truth import Truth\n",
    "",
)

text = text.replace(
'''class InformationConflict(InformationError):
    """An information state contains both P and NOT P."""


''',
    "",
)

start = text.index("class InformationState:")
end = text.index("\n\ndef format_proposition(", start)

replacement = '''class InformationState:
    """Open-world collection of represented Propositions.

    Presence means represented, not true.

    Absence means not represented, not false.

    P and NOT P may coexist because representation does not itself
    determine truth or epistemic warrant.
    """

    def __init__(
        self,
        *propositions: Proposition,
    ) -> None:
        self._propositions: list[
            Proposition
        ] = []

        for proposition in propositions:
            self.add(
                proposition
            )

    @property
    def propositions(
        self,
    ) -> tuple[Proposition, ...]:
        return tuple(
            self._propositions
        )

    def add(
        self,
        proposition: Proposition,
    ) -> None:
        if proposition not in self._propositions:
            self._propositions.append(
                proposition
            )

    def contains(
        self,
        proposition: Proposition,
    ) -> bool:
        return (
            proposition
            in self._propositions
        )

    def contains_negation(
        self,
        proposition: Proposition,
    ) -> bool:
        return self.contains(
            negate(proposition)
        )

    def polarity(
        self,
        proposition: Proposition,
    ) -> tuple[bool, bool]:
        """Return represented positive and negative forms.

        The tuple is:

            (
                P represented,
                NOT P represented,
            )

        This is representational state only.

        It is not Truth and not epistemic Support.
        """

        return (
            self.contains(
                proposition
            ),
            self.contains_negation(
                proposition
            ),
        )
'''

text = (
    text[:start]
    + replacement
    + text[end:]
)

text = text.replace(
    '    "InformationConflict",\n',
    "",
)

path.write_text(text)
PY

cat > src/veridic/interpretation.py <<'PY'
"""Truth evaluation boundary.

A Proposition is truth-apt Information.

Its presence in Veridic does not establish its Truth.

Truth is produced only by evaluation under an Interpretation:

    Proposition + Interpretation -> Truth
"""

from __future__ import annotations

from typing import Protocol

from .information import Proposition
from .utilities.truth import Truth


class Interpretation(Protocol):
    """Something capable of evaluating a Proposition."""

    def evaluate(
        self,
        proposition: Proposition,
    ) -> Truth:
        """Evaluate a Proposition under this Interpretation."""


def evaluate_truth(
    proposition: Proposition,
    *,
    under: Interpretation,
) -> Truth:
    """Evaluate truth explicitly under an Interpretation."""

    result = under.evaluate(
        proposition
    )

    if not isinstance(
        result,
        Truth,
    ):
        raise TypeError(
            "Interpretation.evaluate() must return Truth"
        )

    return result


__all__ = [
    "Interpretation",
    "evaluate_truth",
]
PY

python - <<'PY'
from pathlib import Path

path = Path("src/veridic/utilities/truth.py")
text = path.read_text()

text = text.replace(
    '"""Three-valued epistemic truth."""',
    '"""Three-valued result of Proposition truth evaluation."""',
)

text = text.replace(
    '"""A proposition may be true, false, or unresolved."""',
    '"""Truth evaluation may be true, false, or unresolved."""',
)

path.write_text(text)
PY

cat > tests/test_information_model.py <<'PY'
from veridic.catalog import (
    DURATION,
    TIMESTAMP_START,
)
from veridic.field import FieldValue
from veridic.information import (
    InformationState,
    conjunction,
    negate,
    value_statement,
)


def proposition():
    return value_statement(
        FieldValue(
            TIMESTAMP_START,
            10.0,
        )
    )


def test_proposition_exists_without_knowledge():
    information = proposition()

    assert information is not None


def test_present_information_is_represented():
    information = proposition()

    state = InformationState(
        information
    )

    assert state.contains(
        information
    )


def test_absence_means_not_represented():
    information = proposition()

    state = InformationState()

    assert not state.contains(
        information
    )


def test_negative_information_is_separate_representation():
    information = proposition()

    negative = negate(
        information
    )

    state = InformationState(
        negative
    )

    assert not state.contains(
        information
    )

    assert state.contains(
        negative
    )

    assert (
        state.polarity(
            information
        )
        == (
            False,
            True,
        )
    )


def test_compound_information_can_be_represented():
    first = proposition()

    second = value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )

    compound = conjunction(
        first,
        second,
    )

    state = InformationState(
        compound
    )

    assert state.contains(
        compound
    )


def test_opposing_information_is_preserved_without_truth_collapse():
    information = proposition()

    state = InformationState(
        information,
        negate(information),
    )

    assert (
        state.polarity(
            information
        )
        == (
            True,
            True,
        )
    )
PY

cat > tests/test_interpretation.py <<'PY'
from veridic.catalog import DURATION
from veridic.field import FieldValue
from veridic.information import value_statement
from veridic.interpretation import evaluate_truth
from veridic.utilities.testing import raises
from veridic.utilities.truth import Truth


def proposition():
    return value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )


class TrueInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return Truth.TRUE


class FalseInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return Truth.FALSE


class UnknownInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return Truth.UNKNOWN


class InvalidInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return "true"


def test_truth_requires_interpretation():
    p = proposition()

    assert (
        evaluate_truth(
            p,
            under=TrueInterpretation(),
        )
        is Truth.TRUE
    )

    assert (
        evaluate_truth(
            p,
            under=FalseInterpretation(),
        )
        is Truth.FALSE
    )

    assert (
        evaluate_truth(
            p,
            under=UnknownInterpretation(),
        )
        is Truth.UNKNOWN
    )


def test_interpretation_must_return_truth():
    with raises(TypeError):
        evaluate_truth(
            proposition(),
            under=InvalidInterpretation(),
        )
PY

cat > tests/test_truth_vs_support.py <<'PY'
from veridic.catalog import DURATION
from veridic.domain_laws import (
    build_domain_runtime,
)
from veridic.field import FieldValue
from veridic.information import (
    InformationState,
    negate,
    value_statement,
)
from veridic.interpretation import evaluate_truth
from veridic.knowledge import Provenance
from veridic.knowledge_model import (
    KnowledgeBase,
)
from veridic.support import SupportState
from veridic.utilities.truth import Truth


def proposition():
    return value_statement(
        FieldValue(
            DURATION,
            5.0,
        )
    )


class UnknownInterpretation:
    def evaluate(
        self,
        proposition,
    ):
        return Truth.UNKNOWN


def test_truth_enum_remains_three_valued():
    assert set(Truth) == {
        Truth.TRUE,
        Truth.FALSE,
        Truth.UNKNOWN,
    }


def test_representation_does_not_imply_truth():
    p = proposition()

    information = InformationState(
        p
    )

    assert information.contains(p)

    assert (
        evaluate_truth(
            p,
            under=UnknownInterpretation(),
        )
        is Truth.UNKNOWN
    )


def test_truth_and_knowledge_support_are_distinct():
    p = proposition()

    knowledge = KnowledgeBase(
        build_domain_runtime()
    )

    knowledge.assert_information(
        "K:P",
        p,
        provenance=Provenance(
            source="source-A"
        ),
    )

    knowledge.assert_information(
        "K:not-P",
        negate(p),
        provenance=Provenance(
            source="source-B"
        ),
    )

    assert (
        evaluate_truth(
            p,
            under=UnknownInterpretation(),
        )
        is Truth.UNKNOWN
    )

    assert (
        knowledge.support(p).state
        is SupportState.BOTH
    )


def test_both_support_does_not_create_arbitrary_knowledge():
    p = proposition()

    q = value_statement(
        FieldValue(
            DURATION,
            8.0,
        )
    )

    knowledge = KnowledgeBase(
        build_domain_runtime()
    )

    knowledge.assert_information(
        "K:P",
        p,
        provenance=Provenance(
            source="source-A"
        ),
    )

    knowledge.assert_information(
        "K:not-P",
        negate(p),
        provenance=Provenance(
            source="source-B"
        ),
    )

    assert (
        knowledge.support(p).state
        is SupportState.BOTH
    )

    assert (
        knowledge.support(q).state
        is SupportState.NEITHER
    )
PY

python - <<'PY'
from pathlib import Path

path = Path(
    "docs/theory/data-information-knowledge.md"
)

text = path.read_text()

old = """# Open World

Absence of Information is not negative Information.

    absence(P)
        !=
    NOT P

If neither P nor NOT P is represented, evaluation is:

    UNKNOWN

This preserves Veridic's existing epistemic distinction:

    TRUE
    FALSE
    UNKNOWN
"""

new = """# Open World

Absence of Information is not negative Information.

    absence(P)
        !=
    NOT P

Representation and Truth are distinct.

If neither P nor NOT P is represented, Veridic has no represented
information about either polarity.

This does not itself assign a Truth value.

Truth requires evaluation under an Interpretation:

    Proposition
        +
    Interpretation
        ->
    Truth

Therefore:

    represented(P)
        !=
    true(P)

and:

    absent(P)
        !=
    false(P)
"""

if old not in text:
    raise SystemExit(
        "Open World documentation anchor not found"
    )

path.write_text(
    text.replace(
        old,
        new,
    )
)
PY

cat > docs/theory/representation-warrant-truth.md <<'EOF'
# Representation, Warrant, and Truth

Veridic distinguishes three questions that must not collapse.

## Representation

    Is Proposition P represented?

Representation belongs to the Information Model.

An InformationState stores represented Propositions.

Presence means only:

    represented(P)

It does not imply:

    true(P)

or:

    warranted(P)

Likewise, absence means:

    not represented(P)

It does not imply:

    false(P)

---

# Warrant

    Why may Veridic epistemically hold P?

Warrant belongs to the Knowledge Model.

    Knowledge
        =
    Proposition + Warrant

where:

    Warrant
        =
    Assertion | Derivation

Thus:

    represented(P)
        !=
    warranted(P)

A Proposition may exist as Information without becoming Knowledge.

---

# Truth

    Does P obtain under an Interpretation?

Truth is not inferred from representation or warrant.

The executable boundary is:

    Proposition
        +
    Interpretation
        ->
    Truth

with:

    Truth
        =
    TRUE | FALSE | UNKNOWN

Truth therefore depends on an Interpretation.

The Interpretation may represent:

    a modeled world
    an authoritative state
    an external oracle
    an evaluation environment
    a formal model

Veridic does not yet privilege one Interpretation type.

---

# Opposing Representation

An InformationState may contain both:

    P

and:

    NOT P

without error.

This means only that both propositions are represented.

It does not mean:

    P is both true and false

and it does not mean:

    both propositions are warranted

Those questions belong to Truth and Knowledge respectively.

---

# Opposing Warrant

Knowledge may independently warrant:

    P

and:

    NOT P

That produces:

    Support(P) = BOTH

BOTH is an epistemic support state.

It remains separate from Truth.

---

# Reduced Semantics

The foundational spine remains:

    Data
        ->
    Information
        ->
    Knowledge

Truth is orthogonal:

    Proposition
        ->
    Interpretation
        ->
    Truth

Support and Lineage remain derived analyses over Knowledge.

Therefore:

    Representation
        !=
    Warrant
        !=
    Truth

This distinction is now executable rather than merely conceptual.

## Representation, Warrant, and Truth

Veridic distinguishes three independent questions:

```text
represented(P)?
warranted(P)?
true(P under Interpretation)?

Representation belongs to Information, Warrant belongs to Knowledge,
and Truth is produced only by evaluating a Proposition under an
Interpretation.

Propositi
Representation belongs to Information, Warrant belongs to Knowledge,
and Truth is produced only by evaluating a Proposition under an
Interpretation.

Proposition + Interpretation -> Truth

Neither represented Information nor epistemic Support is silently
promoted to Truth.
