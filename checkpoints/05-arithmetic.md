Checkpoint 05 – Arithmetic and Logic Unit (ALU)

Objective
Implement full 8-bit arithmetic and logical operations, including correct flag behavior.

Overview

At this stage the emulator transitions from basic instruction flow into real computation. Arithmetic in CHIP-8 is strictly 8-bit. Every register (V0–VF) must behave as an unsigned 8-bit value. Any operation that exceeds this range must wrap around modulo 256.

Incorrect arithmetic is one of the most common reasons otherwise functional emulators fail compatibility tests.

Instructions to Implement

7XNN – Add NN to VX (no carry flag modification)
8XY0 – VX = VY
8XY1 – VX = VX OR VY
8XY2 – VX = VX AND VY
8XY3 – VX = VX XOR VY
8XY4 – VX = VX + VY, set VF = carry
8XY5 – VX = VX − VY, set VF = NOT borrow
8XY6 – Shift right
8XY7 – VX = VY − VX, set VF = NOT borrow
8XYE – Shift left

Critical Behavioral Details

8-bit Wrapping

All arithmetic results must be masked to 8 bits.
Example: 255 + 1 becomes 0.
Example: 0 − 1 becomes 255.

Carry Logic (8XY4)

If VX + VY > 255, then:
VF = 1
Otherwise:
VF = 0

The result stored in VX is truncated to 8 bits.

Borrow Logic (8XY5, 8XY7)

For subtraction:

VF = 1 if no borrow occurs
VF = 0 if borrow occurs

Common mistake: comparing with “>” instead of “>=”.

Shift Ambiguity

There are two historical interpretations:

Modern interpreters:
Shift VX directly.

Original COSMAC VIP behavior:
Use VY as source and store result in VX.

You must choose one implementation and document it. Silent mixing causes compatibility problems.

Validation

Create micro-ROM tests that:

Add values that overflow.

Subtract values that underflow.

Confirm VF behavior explicitly.

Shift values with MSB and LSB set.

Confirm wraparound is correct in every case.

Common Mistakes

Forgetting to mask results to 8 bits.

Incorrect borrow logic.

Not clearing or setting VF explicitly.

Letting Python integers exceed 255 silently.

Implementing only first-nibble matching without validating full opcode.

Checkpoint Completion Criteria

All arithmetic behaves deterministically at edge values.

VF behaves correctly for add and subtract.

Shift behavior is consistent and documented.

No silent overflow beyond 8-bit range.