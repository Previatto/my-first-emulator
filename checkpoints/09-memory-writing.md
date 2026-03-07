# Checkpoint 09 – Memory and Register Transfers

## Objective

Implement structured memory and register transfer instructions.

These instructions allow programs to move data between:

- Registers
- Memory
- The index register (I)

They are commonly used for sprite addressing, saving state, and numeric conversion.

Incorrect implementation frequently causes subtle memory corruption.

---

# Instructions to Implement

## FX1E – Add VX to I

Behavior:


I = I + VX


This instruction modifies the index register by adding the value stored in VX.

Important considerations:

- I may exceed typical memory bounds if not validated.
- VF is **not modified** by this instruction in most modern implementations.

---

## FX29 – Font Sprite Address

Behavior:


I = location of font sprite for digit VX


CHIP-8 fonts are stored in memory as sprites representing digits:


0 1 2 3 4 5 6 7 8 9 A B C D E F


Each font character is typically **5 bytes tall**.

Therefore the address calculation becomes:


I = font_base + (VX * 5)


Where:


font_base = starting address of font data


Most interpreters store fonts at:


0x050


You must ensure VX contains a valid hexadecimal digit (0–15).

---

## FX33 – Binary-Coded Decimal (BCD)

Behavior:

Store the decimal digits of VX into memory.

Example:


VX = 234


Then:


memory[I] = 2
memory[I+1] = 3
memory[I+2] = 4


Conversion method:


hundreds = VX // 100
tens = (VX // 10) % 10
ones = VX % 10


Store each digit in separate memory locations.

This instruction is commonly used for displaying scores.

---

## FX55 – Store Registers in Memory

Behavior:


memory[I] through memory[I+X] = V0 through VX


This operation copies registers sequentially.

Example:


X = 3


Result:


memory[I] = V0
memory[I+1] = V1
memory[I+2] = V2
memory[I+3] = V3


Important:

The register range is **inclusive**.

---

## FX65 – Load Registers From Memory

Behavior:


V0 through VX = memory[I] through memory[I+X]


Example:


X = 3


Result:


V0 = memory[I]
V1 = memory[I+1]
V2 = memory[I+2]
V3 = memory[I+3]


Again, the range is **inclusive**.

---

# I Register Behavior

There are two historical behaviors for FX55 and FX65.

### Original COSMAC VIP Behavior

After execution:


I = I + X + 1


### Modern Interpreter Behavior


I remains unchanged


Both behaviors exist in the ecosystem.

You must:

- Choose one implementation
- Document the behavior clearly

Most modern emulators keep **I unchanged**.

---

# Validation Strategy

## Register Storage Test

1. Set several registers to known values.
2. Execute `FX55`.
3. Inspect memory.

Expected:

Registers appear sequentially in memory.

---

## Register Load Test

1. Pre-fill memory.
2. Execute `FX65`.
3. Verify registers load correctly.

---

## BCD Test

Set:


VX = 123


Expected memory result:


memory[I] = 1
memory[I+1] = 2
memory[I+2] = 3


---

## Font Address Test

Set:


VX = 5


Expected:


I = font_base + (5 * 5)


Confirm sprite data corresponds to digit `5`.

---

# Common Mistakes

- Off-by-one errors in FX55/FX65 loops
- Forgetting that register range is inclusive
- Accidentally modifying I when not intended
- Miscomputing BCD digits
- Reading/writing memory outside bounds
- Using incorrect font offset

---

# Checkpoint Completion Criteria

You are complete when:

- FX1E correctly adds VX to I
- FX29 locates correct font sprite addresses
- FX33 stores accurate BCD digits
- FX55 stores registers correctly
- FX65 loads registers correctly
- No unintended memory corruption occurs
- I register behavior is consistent and documented

At this point, your emulator supports:

- Memory transfers
- Register serialization
- Font addressing
- Numeric conversion

Your CHIP-8 virtual machine is now feature-complete.
