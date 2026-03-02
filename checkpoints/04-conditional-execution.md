Checkpoint 04 – Conditional Execution (Skip Instructions)

Objective
Implement conditional branching using skip instructions.

These instructions allow the program to decide what to execute next.

Concept of “Skip”

Instead of jumping somewhere else, CHIP-8 often skips the next instruction.

Because each instruction is 2 bytes:

Skipping means:

PC = PC + 2

This happens only if a condition is true.

Instructions to Implement

3XNN – Skip if VX == NN
4XNN – Skip if VX != NN
5XY0 – Skip if VX == VY
9XY0 – Skip if VX != VY

Behavior Details

If condition is true:

PC = PC + 2

If false:

Do nothing (normal flow continues)

Remember:

PC was already incremented after fetch.

So a successful skip advances PC by 4 total from original instruction location.

Important Validation Rule

5XY0 and 9XY0 are only valid when the last nibble is 0.

Example:

0x5230 → valid
0x5231 → invalid

Validate full opcode pattern, not just first nibble.

Mental Example

If memory contains:

200: 6005 ; V0 = 5
202: 3005 ; Skip if V0 == 5
204: 6101 ; V1 = 1
206: 6102 ; V1 = 2

Because V0 == 5:

Instruction at 204 is skipped.
V1 becomes 2.

Validation

Write a small ROM that:

Sets registers

Uses equality and inequality skips

Verifies correct instruction flow

Test both true and false cases.

Common Mistakes

Skipping even when condition is false

Forgetting that PC already incremented

Incorrect nibble extraction

Not validating final nibble for 5XY0 and 9XY0

Silent acceptance of malformed opcodes

Checkpoint Complete When

All four skip instructions work correctly

PC increments exactly as expected

Invalid opcode patterns are detected

Branching logic behaves predictably

At this point, your emulator supports:

Sequential execution

Jumps

Subroutine calls

Conditional branching

You now have a fully functional control flow system.