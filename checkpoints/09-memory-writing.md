Checkpoint 09 – Memory and Register Transfers

Objective
Implement structured memory/register transfer instructions.

Instructions

FX1E – I += VX
FX29 – Set I to font sprite address for digit in VX
FX33 – Store BCD representation of VX at I, I+1, I+2
FX55 – Store V0 through VX in memory starting at I
FX65 – Load V0 through VX from memory starting at I

Critical Details

Inclusive Range

FX55 and FX65 operate from V0 to VX inclusive.

I Register Behavior

Original interpreters increment I after FX55/FX65.
Modern interpreters often do not.

Choose behavior and document it.

BCD Conversion

Example:
VX = 234
memory[I] = 2
memory[I+1] = 3
memory[I+2] = 4

Validation

Test storing and loading full register sets.

Confirm BCD conversion correctness.

Verify no unintended I modification.

Confirm font addressing is correct.

Common Mistakes

Off-by-one errors.

Forgetting inclusive range.

Corrupting I unexpectedly.

Miscomputing BCD digits.