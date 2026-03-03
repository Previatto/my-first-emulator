# How to Extract CHIP-8 Instruction Fields (Nibble Guide)

If opcode decoding feels confusing, this guide breaks it down step by step.

CHIP-8 instructions are always **16 bits long** (2 bytes).

Example instruction:


0x6A0F


In binary, that looks like:


0110 1010 0000 1111


Each group of 4 bits is called a **nibble**.

So a CHIP-8 instruction is:


NNNN XXXX YYYY ZZZZ


Or in simpler terms:


[first][second][third][fourth]
nibble nibble nibble nibble


---

## Step 1 – Understand Bit Positions

A 16-bit number looks like this:


15 .............. 0


Bit 15 is the leftmost bit.  
Bit 0 is the rightmost bit.

When you shift right (`>>`), you move bits toward the right, discarding lower bits.

When you use a bitmask (`&`), you keep only specific bits.

---

## Visual Layout of a CHIP-8 Instruction


Bits: 15-12 11-8 7-4 3-0
---- ---- ---- ----
N1 N2 N3 N4


Where:

- N1 = first nibble
- N2 = second nibble
- N3 = third nibble
- N4 = fourth nibble

Example:


Instruction: 0x6A0F

Binary:
0110 1010 0000 1111

N1 = 0110 = 6
N2 = 1010 = A
N3 = 0000 = 0
N4 = 1111 = F


---

# Extracting Each Part

## First Nibble (Instruction Group)

Shift right by 12 bits:


instruction >> 12


Why?

Because bits 15–12 become bits 3–0 after shifting.

Example:


0x6A0F >> 12 = 0x6


This tells you which major instruction group you are in.

---

## Second Nibble (X)

Shift right 8 bits, then keep only the last 4 bits:


(instruction >> 8) & 0xF


Why `& 0xF`?

Because `0xF` in binary is:


0000 1111


It keeps only the lowest 4 bits.

Example:


0x6A0F >> 8 = 0x6A
0x6A & 0xF = 0xA


So X = A.

---

## Third Nibble (Y)

Shift right 4 bits, then mask:


(instruction >> 4) & 0xF


Example:


0x6A0F >> 4 = 0x6A0
0x6A0 & 0xF = 0x0


So Y = 0.

---

## Last Nibble (N)

Mask only the lowest 4 bits:


instruction & 0xF


Example:


0x6A0F & 0xF = 0xF


---

## Last Two Hex Digits (NN)

Mask the lowest 8 bits:


instruction & 0xFF


`0xFF` in binary:


1111 1111


Example:


0x6A0F & 0xFF = 0x0F


---

## Last Three Hex Digits (NNN)

Mask the lowest 12 bits:


instruction & 0x0FFF


`0x0FFF` in binary:


0000 1111 1111 1111


Example:


0x6A0F & 0x0FFF = 0xA0F


---

# Why This Works

Bit shifting moves the desired nibble into the lowest 4-bit position.

Bit masking removes everything else.

Decoding is simply:

1. Shift to align
2. Mask to isolate

Nothing more.

---

# Mental Model

Think of the 16-bit instruction as four small boxes:


[ N1 ][ N2 ][ N3 ][ N4 ]


You are just selecting which box you want.

- Shift moves the box to the right edge.
- Mask cuts off everything else.

---

# Common Mistakes

- Forgetting to mask after shifting
- Using wrong mask (e.g., `0xFF` instead of `0xF`)
- Mixing up NN (8 bits) and NNN (12 bits)
- Confusing hexadecimal digits with decimal digits

---

# Final Reminder

CHIP-8 decoding is not complicated.

It is consistent bit slicing.

If decoding feels confusing, write down the binary form of one instruction and label the nibble boundaries manually.

Once it clicks, every opcode follows the same structure.
