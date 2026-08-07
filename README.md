# FieldFrame

**A field-aware semantic DataFrame runtime.**

FieldFrame is a research and engineering project exploring a layered and
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

A FieldFrame operation should be able to determine:

1. whether an operation is representationally executable;
2. whether the operation is semantically meaningful;
3. what Field semantics the result acquires; and
4. whether contextual invariants remain satisfied.

The initial computational model is:

    Admit -> Execute -> Transfer -> Verify

FieldFrame is currently experimental research. The field hierarchy,
operation algebra, and runtime semantics are not yet considered stable.
