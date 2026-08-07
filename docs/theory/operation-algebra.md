# Field Operation Algebra

## Purpose

Define the semantic admission and transfer rules for operations over Fields.

## Evaluation Pipeline

    Resolve
      |
      v
    Admit
      |
      v
    Execute
      |
      v
    Transfer
      |
      v
    Verify

## Validity Levels

### Representational Validity

Can the underlying runtime execute the operation?

### Semantic Validity

Does the meaning of the Field admit the operation?

### Contextual Validity

Does the resulting Field continue to satisfy its Role and Invariants?

## Initial Operators

- EQ
- NE
- LT
- LE
- GT
- GE
- ADD
- SUB
- MUL
- DIV
- COUNT
- SUM
- MEAN
- MIN
- MAX
- GROUP
- JOIN
- CAST
- CONVERT_UNIT

## Example Rules

    Timestamp - Timestamp -> Duration

    ByteCount / Duration -> DataRate

    PacketCount / Duration -> PacketRate

    IPv4Address + IPv4Address -> undefined

    MEAN(IPv4Address) -> undefined
