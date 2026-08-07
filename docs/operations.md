# Veridic Operations

Veridic now provides an operational command-line surface.

The CLI is intentionally thin.

It does not reimplement semantic logic.

It exposes the existing Veridic runtime.

## Field Catalog

    ./bin/veridic fields

Inspect one Field:

    ./bin/veridic show event.duration

## Semantic Resolution

Resolve whether an operation is meaningful without supplying values:

    ./bin/veridic resolve sub event.end event.start

Veridic reports:

    operation
    admission
    governing rule
    input Field semantics
    output Field semantics

An undefined semantic operation exits non-zero.

## Semantic Computation

Execute an admitted operation:

    ./bin/veridic compute sub event.end=15.0 event.start=10.0

The result is a derived Duration Field:

    (event.end-event.start) = 5.0 s

Derivation does not silently imply contextual binding.

To bind the result into the contextual Event Duration Field:

    ./bin/veridic compute sub --as event.duration event.end=15.0 event.start=10.0

That binding activates the target Field invariants using the supplied
operand context.

Therefore computation distinguishes:

    representational execution
    semantic admission
    contextual validity

## Derived Rates

Example:

    ./bin/veridic compute div network.bytes=10000.0 event.duration=5.0

This derives a DataRate through Veridic's existing semantic and unit
algebra.

## Invalid Meaning

This request is numerically representable but semantically undefined:

    ./bin/veridic compute add source.ip=192.0.2.1 destination.ip=198.51.100.1

Veridic rejects it before pretending that successful host-language
computation implies meaningful computation.

## Contextual Failure

This operation is semantically admitted:

    ./bin/veridic compute sub --as event.duration event.end=5.0 event.start=10.0

The derivation itself is semantically valid, but binding it as
event.duration yields a negative contextual Duration.

The target Field invariant rejects the binding contextually.

The CLI uses a distinct exit code for this case.

## Exit Codes

    0
        successful semantic computation

    2
        invalid request, undefined semantic operation, or execution error

    3
        computation executed but output invariants were violated

## JSON

Machine-readable output is available with:

    ./bin/veridic --json compute sub --as event.duration event.end=15.0 event.start=10.0

This makes Veridic usable from shell scripts and other programs without
adding a third-party dependency.

## Installed Command

The package also defines:

    veridic = veridic.cli:main

When Veridic is installed as a Python package, the same interface is
available as:

    veridic fields
    veridic show event.duration
    veridic resolve sub event.end event.start
    veridic compute sub event.end=15.0 event.start=10.0
    veridic compute sub --as event.duration event.end=15.0 event.start=10.0

## Derivation vs Binding

Veridic does not equate semantic derivation with contextual placement.

    derive
        ->
    Derived.Duration

is distinct from:

    bind as event.duration
        ->
    Event.Duration

The derived Field establishes what the result means.

The target Field establishes where that result is being asserted to
belong.

Contextual invariants are therefore evaluated only after an explicit
binding target is supplied.

This preserves:

    semantic validity
        !=
    contextual validity
