# Checkpoint 04 – Conditional Execution (Skip Instructions)

## Objective

Implement conditional branching using skip instructions.

Unlike jumps, CHIP-8 commonly changes flow by **skipping the next instruction** if a condition is true.


---

## The Concept of “Skip”

Remember: Each CHIP-8 instruction is 2 bytes.

If a condition is true:


PC = PC + 2


Because the PC was already incremented during fetch, a successful skip moves execution forward by 4 bytes total from the original instruction.

If the condition is false:

Do nothing. Execution continues normally.

---

## Instructions to Implement

### 3XNN – Skip if VX == NN

If:

VX == NN

Then:

PC += 2


---

### 4XNN – Skip if VX != NN

If:

VX != NN

Then:

PC += 2


---

### 5XY0 – Skip if VX == VY

If:

VX == VY

Then:

PC += 2


Important:
This instruction is valid **only if the last nibble is 0**.

Example:

0x5230 → valid
0x5231 → invalid


You must validate the entire opcode pattern.

---

### 9XY0 – Skip if VX != VY

If:

VX != VY

Then:

PC += 2


Also valid only if the last nibble is 0.

---

## Implementation Pattern

For each skip instruction:

1. Extract required nibbles (X, Y, NN).
2. Evaluate the condition.
3. If true → `PC += 2`
4. If false → do nothing.


---

## Mental Example

Memory:


200: 6005 ; V0 = 5
202: 3005 ; Skip if V0 == 5
204: 6101 ; V1 = 1
206: 6102 ; V1 = 2


Execution:

- V0 becomes 5.
- Condition at 202 is true.
- Instruction at 204 is skipped.
- V1 becomes 2.

Final result:

V0 = 5
V1 = 2


---

## Test ROM (Covers All Skip Types)

You can use the test rom `conditional_instructions.ch8`.

### Expected Final Register State


V0 = 5
V1 = 5
V2 = 3
V3 = 2
V4 = 1
V5 = 2
V6 = 2


If any value differs, your skip logic is incorrect.


If you are curious, this is the code for rom `conditional_instructions.ch8`:

; ===== Setup =====
200: 6005 ; V0 = 5
202: 6105 ; V1 = 5
204: 6203 ; V2 = 3

; ===== 3XNN (true case) =====
206: 3005 ; Skip if V0 == 5 (true)
208: 6301 ; V3 = 1 (should be skipped)
20A: 6302 ; V3 = 2

; ===== 4XNN (false case) =====
20C: 4005 ; Skip if V0 != 5 (false)
20E: 6401 ; V4 = 1

; ===== 5XY0 (true case) =====
210: 5010 ; Skip if V0 == V1 (true)
212: 6501 ; V5 = 1 (should be skipped)
214: 6502 ; V5 = 2

; ===== 9XY0 (true case) =====
216: 9020 ; Skip if V0 != V2 (true, 5 != 3)
218: 6601 ; V6 = 1 (should be skipped)
21A: 6602 ; V6 = 2

; ===== Loop =====
21C: 121C ; Infinite loop


You would have to save it and compile it for chip-8, so we are skipping it for now.

---

## Critical Validation Rules

You must:

- Ensure `5XY0` only executes when last nibble is 0
- Ensure `9XY0` only executes when last nibble is 0
- Detect and reject malformed opcodes
- Not skip when condition is false
- Not increment PC twice accidentally

If opcode is malformed:
Print error and halt execution.

Silent failure makes debugging extremely difficult.

---


## Checkpoint Complete When

- All four skip instructions behave correctly
- PC advances exactly as expected
- Invalid opcode patterns are rejected
- True and false cases behave predictably
- Nested skips work properly

At this stage, your emulator now supports:

- Sequential execution
- Jumps
- Subroutine calls
- Conditional branching

You now have a complete and functional control flow system.
