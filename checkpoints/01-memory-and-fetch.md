Checkpoint 01 – Memory Loading and Instruction Fetching

Objective
Load a ROM into memory and implement correct instruction fetching.

You are not executing instructions yet. You are only preparing the system to read them correctly.

What You Should Already Have (From Checkpoint 00)

4096-byte memory

PC initialized to 0x200

Registers defined

Stack defined

Now you will make memory usable.

Step 1 – Loading a ROM into Memory

A CHIP-8 ROM is simply a sequence of bytes.

When loading a ROM:

Copy its bytes into memory

Start writing at address 0x200

Do not overwrite memory below 0x200

Conceptually:

memory[0x200] = first byte of ROM
memory[0x201] = second byte
memory[0x202] = third byte
…

Do not modify PC here. It should already be 0x200.

Step 2 – Fetching an Instruction

Each CHIP-8 instruction is exactly 2 bytes.

To fetch:

Read the byte at memory[PC]

Read the byte at memory[PC + 1]

Combine them into one 16-bit number

Important: CHIP-8 is big-endian.

This means:

instruction = (first_byte << 8) | second_byte

After fetching:

PC = PC + 2

The increment happens after reading the instruction.

Mental Model

If memory contains:

Address 0x200 → 0x60
Address 0x201 → 0x0A

The instruction is:

0x600A

Not:

0x0A60

Fetch–Only Loop (Temporary)

At this stage, you may write a simple loop that:

Fetches instruction

Prints instruction in hexadecimal

Advances PC

Stops at end of ROM

You are not decoding yet.

Validation

Load a known ROM.

Print instructions sequentially.

Verify alignment: instructions must not shift or misread.

Confirm PC increments by 2 each time.

If instructions look corrupted, suspect:

Incorrect endianness

Wrong PC initialization

Incorrect ROM loading offset

Common Mistakes

Starting PC at 0x000

Incrementing PC before reading bytes

Reading only one byte per instruction

Combining bytes in little-endian order

Allowing PC to run beyond ROM bounds

Checkpoint complete when:

ROM loads correctly at 0x200

Fetch returns valid 16-bit instructions

PC advances exactly 2 bytes per fetch

Do not proceed until instruction fetching is correct.
