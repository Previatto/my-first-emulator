# Checkpoint 07 – Input Handling

[EDITOR NOTE: ADD CXKK here too]

## Objective

Implement keypad input and input-based control flow.

This stage connects your emulator to real interaction. Incorrect input handling commonly causes programs to freeze, skip incorrectly, or behave nondeterministically.

---

## CHIP-8 Keypad Model

CHIP-8 defines a 16-key hexadecimal keypad:


1 2 3 C
4 5 6 D
7 8 9 E
A 0 B F


Keys are logical values:


0x0 – 0xF


You must map physical keyboard keys to these 16 logical keys. The mapping must remain consistent throughout execution.

A common layout (recommended):


Keyboard: CHIP-8:
1 2 3 4 1 2 3 C
Q W E R → 4 5 6 D
A S D F 7 8 9 E
Z X C V A 0 B F


You may choose another layout, but document it.

---

# Instructions to Implement

## EX9E – Skip if Key in VX Is Pressed

Behavior:

If:


keypad[VX] == pressed


Then:


PC += 2


Remember:

PC was already incremented during fetch.

---

## EXA1 – Skip if Key in VX Is Not Pressed

If:


keypad[VX] == not pressed


Then:


PC += 2


---

## Important Validation

VX must contain a valid key index:


0 <= VX <= 15


If VX is outside this range:

- Print error
- Halt execution

Do not index outside keypad array.

---

# FX0A – Wait for Key Press

This instruction blocks execution until a key is pressed.

Behavior:

1. Pause instruction execution.
2. When a key is pressed:

VX = key_value

3. Resume execution at next instruction.

---

## Critical Execution Detail

During FX0A:

- Do NOT continue advancing PC.
- Do NOT repeatedly re-execute the instruction.
- Do NOT freeze the entire application loop.

Correct model:

- The CPU stops progressing.
- The emulator continues polling events.
- When a key press occurs, store the value and advance PC.

Incorrect handling causes:
- Infinite loops
- Immediate auto-skipping
- Unresponsive window

---

# Implementation Strategy

Maintain:


keypad[16] → boolean state


On key down:

keypad[key] = True


On key up:

keypad[key] = False


For FX0A:

- Set a "waiting_for_key" flag
- Store which register should receive input
- Only resume when key-down event occurs

---

# Validation ROM Concept

Minimal ROM:


200: F00A ; Wait for key press, store in V0
202: 3001 ; Skip if V0 == 1
204: 1204 ; Loop forever if not key 1
206: 1206 ; Loop forever if key was 1


Expected behavior:

- Emulator halts at 0x200.
- After key press:
  - If key value == 1 → jumps to 0x206
  - Otherwise → loops at 0x204

This confirms:

- FX0A blocks properly
- Skip logic works
- PC increments correctly

---

# Boundary Tests

- Press multiple keys simultaneously.
- Release key before FX0A triggers.
- Set VX manually to invalid value and run EX9E/EXA1.
- Ensure skip only happens when condition is true.

---

# Common Mistakes

- Continuing execution during FX0A
- Incrementing PC repeatedly while waiting
- Ignoring key release events
- Using incorrect key mapping indices
- Not validating VX range
- Polling input incorrectly in event-driven frameworks

---

# Checkpoint Completion Criteria

You are complete when:

- EX9E and EXA1 skip correctly
- FX0A halts execution until key press
- PC increments exactly as expected
- Invalid key indices are handled safely
- Input state updates correctly on press and release

At this stage, your emulator supports:

- Control flow
- Arithmetic logic
- Graphics rendering
- Collision detection
- Real-time user input

Your emulator is now interactive.
