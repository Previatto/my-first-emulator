Checkpoint 06 – Display and Sprite Rendering

Objective
Implement the 64×32 monochrome display and sprite drawing instruction.

Overview

CHIP-8 graphics are minimal but strict. The display is a 64 pixel wide by 32 pixel high grid. Each pixel is either 0 (off) or 1 (on). Rendering is performed exclusively through the DXYN instruction.

This stage introduces bit-level logic and collision detection.

Instruction to Implement

DXYN – Draw sprite at (VX, VY) with height N bytes.

Behavior

Read N bytes starting at memory[I].

Each byte represents one horizontal row.

Each bit in the byte represents one pixel.

Pixels are drawn using XOR logic.

If any pixel changes from 1 to 0, set VF = 1.

Otherwise VF = 0.

Technical Requirements

XOR Drawing

Drawing toggles pixels. It does not overwrite.

Bit Extraction

Each row is 8 bits. You must test each bit individually, typically from MSB to LSB.

Wrapping

Sprites wrap around screen edges horizontally and vertically.

Collision Flag

VF must be cleared before drawing.
Set VF to 1 only if at least one pixel collision occurs.

Display Representation

Use either:

A 2D array [32][64]
or

A flat array of 2048 elements

Ensure coordinate indexing is consistent.

Validation

Test using:

IBM logo ROM

A custom sprite test at screen edges

A collision test (draw sprite twice at same location)

Expected Outcomes

Sprite appears correctly.

Drawing twice erases it.

VF reflects collision correctly.

Wrapping behaves properly.

Common Mistakes

Using OR instead of XOR.

Failing to reset VF before drawing.

Incorrect bit order (LSB/MSB confusion).

Forgetting modulo wrapping.

Indexing errors in 2D grid.