Checkpoint 07 – Input Handling

Objective
Implement keypad input and input-based control flow.

Overview

CHIP-8 uses a 16-key hexadecimal keypad (0–F). Programs rely heavily on input for control logic. Improper input handling causes games to freeze or skip unpredictably.

Instructions to Implement

EX9E – Skip next instruction if key in VX is pressed
EXA1 – Skip next instruction if key in VX is not pressed
FX0A – Wait for key press and store key in VX

Keypad Mapping

You must map physical keyboard keys to the logical 16 keys. The mapping must remain consistent.

Execution Model

EX9E / EXA1

If condition is met, increment PC by 2 again (total skip of 4 bytes).

FX0A

Execution must pause until a key is pressed.
Do not increment PC repeatedly while waiting.

This instruction blocks instruction execution but not the entire application loop.

Validation

Write a ROM that waits for key press.

Confirm that execution halts at FX0A.

Confirm skip instructions alter PC correctly.

Test boundary cases (invalid key index in VX).

Common Mistakes

Continuing execution during FX0A.

Incorrect PC increment logic.

Not checking valid key range.

Polling input incorrectly in event-driven systems.