# Checkpoint 05 – Arithmetic and Logic Unit (ALU)

## Objective

Implement full 8-bit arithmetic and logical operations, including correct flag behavior.

At this stage, your emulator moves from control flow into real computation. Arithmetic in CHIP-8 is strictly 8-bit. Every register (V0–VF) must behave as an unsigned 8-bit value.

This is the moment you will finally have to worry about it.

That means that all results must wrap modulo 256.

If your arithmetic is even slightly incorrect, many ROMs will behave unpredictably.

---

## Core Rule: 8-Bit Wrapping

All arithmetic results must be masked to 8 bits:


result &= 0xFF


Examples:

- 255 + 1 → 0  
- 0 - 1 → 255  

Never allow values larger than 255 to remain in registers.

Python, for example, will not automatically wrap integers. You must enforce it.

Some of these operators will have a "Carry/Borrow flag", it simply means that the result of the sum or subtraction wrapped around the 255 or beyond 0.

---

# Instructions to Implement

## 7XNN – Add NN to VX

Behavior:


VX = (VX + NN) & 0xFF

Note: No Carry Flag yet, just wrap the result

---

# The 8XYZ instructions

They can be a bit annoying to deal with because until now, the first digit defined the behavior, now you have to also check the last digit.


## 8XY0 – VX = VY

Simple assignment:


VX = VY


---

## 8XY1 – OR


VX = VX | VY



---

## 8XY2 – AND


VX = VX & VY



---

## 8XY3 – XOR


VX = VX ^ VY



---

## 8XY4 – Addition With Carry

Here is when we have the carry flag, it will always be attributed to VF, the 16th register.

After the operation is executed, VF should always be set to either 1 or 0.


sum = VX + VY


If:


sum > 255


Then:


VF = 1


Else:


VF = 0


Store:


VX = sum & 0xFF



---

## 8XY5 – Subtract VY From VX


VX = VX - VY


Borrow logic:


VF = 1 if VX >= VY
VF = 0 if VX < VY


Common mistake:

Using `>` instead of `>=`.

Store:


VX = (VX - VY) & 0xFF


---

## 8XY7 – VX = VY - VX

Reverse subtraction.

Borrow logic:


VF = 1 if VY >= VX
VF = 0 if VY < VX


Store:


VX = (VY - VX) & 0xFF


---

## Shift Instructions

There is historical ambiguity.

You must choose and document one behavior.

### Modern Behavior (Recommended)

Shifts operate directly on VX.

### 8XY6 – Shift Right


VF = VX & 0x1
VX = VX >> 1


LSB goes into VF.

---

### 8XYE – Shift Left


VF = (VX >> 7) & 0x1
VX = (VX << 1) & 0xFF


MSB goes into VF.

---

## Critical Implementation Rules

- Always mask results to 8 bits.
- Always explicitly set VF when required.
- Do not leave VF unchanged when instruction specifies behavior.
- Validate full opcode (8XY? pattern), not just first nibble.

---

# Micro Test ROM Concepts

You should build small test programs to verify:

### Addition Overflow

- Set VX = 255
- Add 1 using 8XY4
- Expect VX = 0, VF = 1

### Subtraction Underflow

- VX = 0
- VY = 1
- VX - VY
- Expect VX = 255, VF = 0

### No Borrow Case

- VX = 5
- VY = 5
- VX - VY
- Expect VX = 0, VF = 1

### Shift Right

- VX = 0b00000001
- After shift:
  - VX = 0
  - VF = 1

### Shift Left

- VX = 0b10000000
- After shift:
  - VX = 0
  - VF = 1

If any of these fail, your ALU is incorrect.

---

# Common Mistakes

- Forgetting to mask to 8 bits
- Incorrect borrow logic
- Not setting VF explicitly
- Letting Python integers exceed 255
- Ignoring opcode’s final nibble validation
- Mixing COSMAC and modern shift behavior

---

# Checkpoint Completion Criteria

You are complete when:

- All arithmetic wraps correctly at 0 and 255
- Carry logic works for addition
- Borrow logic works for subtraction
- Shift instructions correctly move MSB/LSB into VF
- VF is deterministic and never stale
- No register ever stores values outside 0–255

At this point, your emulator has a functioning 8-bit ALU.

You now support real computation.
