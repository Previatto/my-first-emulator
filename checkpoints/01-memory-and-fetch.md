# Checkpoint 01 – Memory Loading and Instruction Fetching

## Objective

Load a ROM into memory and implement correct instruction fetching.

No instruction executing yet, but you are preparing the system to read them correctly.

---

## Prerequisites (From Checkpoint 00)

Before continuing, you should already have:

- 4096-byte memory
- Program counter (PC) initialized to `0x200`
- Registers defined
- Stack defined

Now you will make memory usable.

---

## Step 1 – Loading a ROM into Memory

A CHIP-8 ROM is simply a sequence of bytes.

When loading a ROM:

- Copy its bytes into memory
- Start writing at address `0x200`
- Do **not** overwrite memory below `0x200`

Conceptually:

memory[0x200] = first byte of ROM

memory[0x201] = second byte

memory[0x202] = third byte

...


Do not modify the program counter here.  
It should already be set to `0x200`.

---

## Step 2 – Fetching an Instruction

Each CHIP-8 instruction is exactly **2 bytes**.

To fetch an instruction:

1. Read the byte at `memory[PC]`
2. Read the byte at `memory[PC + 1]`
3. Combine them into one 16-bit number

Important: CHIP-8 is **big-endian**.

This means that what is called most significant byte (MSB), is stored before the least significat byte (LSB)


The instruction will be the combination of the two bytes:

(first_byte << 8) | second_byte

This notation means that we are shifting (the << operator) `first_byte` by 8 bits (1 byte) and doing an OR (the | operator) operation.

In decimal notaion, it would be similar to:

-Read first_byte = 25
-Read second_byte = 10

instruction = 25 x 10 + 10 = 2510

We are just multiplying the `first_byte` so that we can join it with `second_byte`.

After fetching, increment PC by 2:

PC = PC + 2

---

## Mental Model

If memory contains:

Address 0x200 → 0x60

Address 0x201 → 0x01

The instruction is:

0x6001

Not:

0x0160

And definetely, not 0x61!!

---

## Temporary Fetch-Only Loop

At this stage, you may write a simple loop that:

- Fetches instruction
- Prints instruction in hexadecimal
- Advances PC
- Stops at the end of the ROM

This is purely about verifying memory alignment and fetch correctness.

---

## Validation

To confirm correctness:

- Load the `rom_loading_text.ch8`
- Verify that your loop prints:
      `60 0A`
      `61 0B`
      `62 0C`
      `63 0D`
      `12 00`


## Common Mistakes

- Starting PC at `0x000`
- Incrementing PC before reading bytes
- Reading only one byte per instruction
- Combining bytes in little-endian order
- Combining bytes by summing them
- Allowing PC to run beyond ROM bounds

---

## Checkpoint Complete When

- ROM loads correctly at `0x200`
- Fetch returns valid 16-bit instructions
- PC advances exactly 2 bytes per fetch
- Printed instructions match expected ROM data
