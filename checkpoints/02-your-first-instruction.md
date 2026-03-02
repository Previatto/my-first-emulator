Checkpoint 02 – Decode Structure and First Instructions

Objective
Build the structure that interprets instructions.

You will now convert raw 16-bit numbers into actions.

Step 1 – Extract Instruction Parts

Given a 16-bit instruction, you must extract:

First nibble (instruction group)
instruction >> 12

Second nibble (X)
(instruction >> 8) & 0xF

Third nibble (Y)
(instruction >> 4) & 0xF

Last nibble (N)
instruction & 0xF

Last two hex digits (NN)
instruction & 0xFF

Last three hex digits (NNN)
instruction & 0x0FFF

These fields determine what the instruction does.

Step 2 – Dispatch by First Nibble

Most CHIP-8 instructions can be grouped by their first nibble.

Conceptually:

group = instruction >> 12

Then call the correct handler based on this group.

Do not implement everything yet.

For now, implement only:

1NNN – Jump
6XNN – Set register

Instruction: 1NNN (Jump)

Behavior:

PC = NNN

This overrides normal sequential execution.

Remember:

PC was already incremented during fetch.
You are now replacing it.

Instruction: 6XNN (Set Register)

Behavior:

VX = NN

Where X is the second nibble.

Registers are 8-bit. Values must stay between 0 and 255.

Minimal Execution Loop

You can now build a real loop:

loop:
fetch instruction
increment PC by 2
decode instruction
execute behavior

At this stage, execution is very limited — that is expected.

Validation

Create a small test program manually:

Example sequence:

600A ; V0 = 10
6105 ; V1 = 5
1200 ; jump to 0x200

This should:

Set registers

Loop infinitely

Confirm:

Registers update correctly

PC jumps properly

No misalignment occurs

Common Mistakes

Forgetting that PC already incremented

Modifying PC incorrectly during jump

Using only first nibble without validating full opcode pattern

Ignoring unknown instructions silently

If an instruction is not implemented, print an error and stop execution.

Silent failure makes debugging significantly harder.

Checkpoint complete when:

Instructions are decoded reliably

1NNN correctly changes PC

6XNN correctly modifies registers

Execution loop runs without crashing

Unknown opcodes are detected explicitly

Once this works, you have built a minimal programmable virtual machine.