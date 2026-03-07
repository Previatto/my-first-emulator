# Checkpoint 06 – Display and Sprite Rendering

## Objective

Implement the 64×32 monochrome display and the `DXYN` sprite drawing instruction.

This stage introduces:

- Bit-level rendering
- XOR pixel logic
- Collision detection
- Coordinate wrapping

Graphics in CHIP-8 are simple but precise. Small mistakes produce visibly incorrect output.


add instruction 00e0
add instruction Annn

---

## Display Model

Resolution:


Width = 64 pixels
Height = 32 pixels


Each pixel is:

- 0 → off
- 1 → on

You may represent the display as:

Option A:

display[32][64]


Option B:

display[2048]


Both are valid. Consistency in indexing is critical.

---

# Instruction: DXYN

Draw a sprite at coordinates:


X = VX
Y = VY
Height = N


---

## How Sprite Data Works

- Read **N bytes** starting at `memory[I]`.
- Each byte represents one horizontal row.
- Each bit in the byte represents one pixel.
- Sprites are always 8 pixels wide.

Example sprite byte:


11110000


Means:

- First 4 pixels ON
- Next 4 pixels OFF

---

# Required Behavior

## 1. Clear VF Before Drawing

Before starting:


VF = 0


---

## 2. Extract Each Bit (MSB First)

For each row:


sprite_byte = memory[I + row]


For each column 0–7:


bit = (sprite_byte >> (7 - col)) & 1


MSB is drawn first.

If you reverse bit order, the sprite will appear mirrored.

---

## 3. Apply XOR Logic

Drawing rule:


display_pixel ^= sprite_bit


Important:

- This toggles pixels.
- It does NOT overwrite.
- It does NOT use OR.

---

## 4. Collision Detection

A collision occurs when:


display_pixel == 1
AND
sprite_bit == 1


If XOR turns a pixel from 1 → 0:


VF = 1


Set VF to 1 if at least one collision occurs.

Do not reset VF back to 0 after a collision is detected.

---

## 5. Wrapping Behavior

Coordinates must wrap around screen edges.

Horizontal:


x = (VX + col) % 64


Vertical:


y = (VY + row) % 32


If you forget wrapping, sprites at screen edges will break.

---

# Full Logical Flow

For each row in N:

1. Read sprite byte
2. For each of 8 bits:
   - Extract bit (MSB first)
   - Compute wrapped screen position
   - Check collision
   - Apply XOR

That is the entire rendering model.

---

# Validation Strategy

## Test 1 – Basic Drawing

Draw a small sprite in center of screen.

Confirm:

- Shape appears correctly
- No distortion
- No flipping

---

## Test 2 – XOR Erase

Draw sprite twice at same location.

Expected:

- First draw → visible
- Second draw → erased
- VF = 1 on second draw

If sprite does not disappear, XOR logic is wrong.

---

## Test 3 – Edge Wrapping

Draw sprite near:

- X = 63
- Y = 31

Confirm wrapping:

- Right edge wraps to left
- Bottom wraps to top

---

## Test 4 – Collision Flag

Draw sprite at same location twice.

Expected:

- First draw → VF = 0
- Second draw → VF = 1

If VF is incorrect, collision logic is wrong.

---

# Common Mistakes

- Using OR instead of XOR
- Forgetting to reset VF before drawing
- Extracting bits LSB first
- Not wrapping coordinates
- Incorrect 2D indexing (row/column swapped)
- Writing outside display bounds
- Setting VF incorrectly for every collision instead of once

---

# Expected Outcomes

You are correct when:

- Sprites render cleanly
- Drawing twice erases sprite
- VF correctly indicates collision
- Edge wrapping works perfectly
- No array index errors occur

At this point, your emulator can render graphics.

You now support:

- Full control flow
- Arithmetic logic
- Pixel rendering
- Collision detection

Your emulator is visually functional.
