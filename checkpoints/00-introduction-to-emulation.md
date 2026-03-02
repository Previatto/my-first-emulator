# Checkpoint 00 – What Is an Emulator?

## Objective

Understand what you are building before writing any code.
Then build the internal “hardware” of CHIP-8 purely in memory.


---

## What Is Emulation? (Simple Explanation)

An emulator is a program that pretends to be another computer.

It recreates the “hardware” of a system entirely in software.  

When a CHIP-8 program runs, it expects certain hardware to exist:

- Memory to store data
- Registers to hold temporary values
- A program counter to know which instruction to execute next
- A stack to handle subroutines
- A display to draw pixels
- Timers for delays and sound

Your have to recreate all of that inside your own program.


---


## Mental Model

Think of your emulator as a small virtual computer living inside your program.

You are:

- Moving numbers in memory
- Updating registers
- Changing the program counter
- Flipping pixels
- Managing a tiny stack

Once this internal machine behaves correctly, games will work automatically.


---


## What CHIP-8 Originally Has

A basic CHIP-8 system contains:

### Memory
- 4096 bytes of RAM

### Registers
- 16 general 8-bit registers (V0–VF)
- 1 index register (I)
- 1 program counter (PC)

### Stack
- 16 levels for subroutine calls
- Stack pointer

### Timers
- Delay timer
- Sound timer

### Graphics
- 64×32 monochrome pixel display

### Input
- 16-key hexadecimal keypad

---

## Translating Hardware to Code (Conceptual)

Here are suggestions on how to simulate the hardware parts of the Chip-8:

### RAM
Represented as a sequence of 4096 numbers.  
Each entry stores one byte (0–255).

### Registers
Represented as a sequence of 16 numbers.

### I Register
A single integer.

### Program Counter (PC)
A single integer.  
Important: It must start at address `0x200`.

### Stack
A sequence with maximum size 16.

### Timers
Two integers that decrease at 60Hz.

### Display
A 64×32 grid of pixels.  
This can be represented as:
- A 2D array  
or  
- A flat array of 2048 elements  
Later, you can use any GUI library to draw scaled pixels.

### Input
- Map your keyboard to 16 CHIP-8 keys.


All register values are 8-bit.  
This means they must wrap around at 255.

---

## Important Detail: Why Programs Start at `0x200`

In the original system, the first 512 bytes (`0x000–0x1FF`) were reserved for the interpreter itself.

Programs were loaded at memory address `0x200`.

Therefore:

- The program counter (PC) must begin at `0x200`.
- If it starts at `0x000`, instructions will be read incorrectly.


---

## The Fetch–Decode–Execute Cycle

Try to understand this:

Conceptual pseudocode:
    loop forever:
        read two bytes from memory at PC
        combine them into one instruction
        increase PC by 2
        decode the instruction
        execute the instruction
    

Every CHIP-8 instruction is 2 bytes long.

The program counter normally moves forward by 2.  
Some instructions modify it directly (jumps, calls, skips).

This cycle is the core of your emulator.

---

## Glossary

**Byte**  
A number between 0 and 255 (8 bits).

**Bit**  
A single binary digit (0 or 1).

**Address**  
A position in memory.

**Opcode**  
The numeric instruction that tells the system what to do.  
Example: `0x6A0F`

**Nibble**  
4 bits (half a byte). Many CHIP-8 instructions are divided into 4 nibbles.

**Hexadecimal**  
Base-16 number system using digits `0–9` and `A–F`.

Examples:
- `0xFF` = 255 in decimal
- `0x200` = 512 in decimal

Hexadecimal is used because memory and binary values map cleanly into base 16.
You will understand when we start reading the instructions.

---

## Checkpoint Complete When

- All hardware components are defined in your program.
- PC is initialized to `0x200`.
- Memory size is exactly 4096 bytes.
- Registers hold only 8-bit values.
- You understand the fetch–decode–execute loop conceptually.

Do not proceed until this structure is clear.    

Now, go pay a visit to [Cowgod's Chip-8 Technical Reference v1.0](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM), it served as my primary source for the layout and instructions.
