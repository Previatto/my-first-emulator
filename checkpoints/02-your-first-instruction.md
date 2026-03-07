# Checkpoint 02 – Decode Structure and First Instructions

## Objective

Build the structure that interprets instructions.

You will now convert raw 16-bit numbers into actions.

At this stage, your emulator stops being a memory reader and becomes a programmable machine.

---

## Step 1 – Extract Instruction Parts


If you haven't by now, you should really pay a visit to [Cowgod's Chip-8 Technical Reference v1.0](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM)!

As you might have recall, the loop of the emulator will something like:

        read two bytes from memory at PC
        combine them into one instruction
        increase PC by 2
        decode the instruction <- we are here
        execute the instruction

It is more simple than you think, each instruction, `0x13A5` for example, can be decoded in a set of parametrized actions.

You just need to extract the information from them. Think of them as a function call and its arguments, but in a very tight manner.

Your code could have a function like:

sum(a, b) -> a + b

the function `sum` and its two argument `a` and `b`. `a + b` defines what the function outputs.



Now, let's examine the instruction `0x13A5`:

For chip-8 you need to check the first nibble first thing:

**First nibble (instruction group)**  

`0x13A5 >> 12 = 1`

The first nibble indentify the type of instruction, and on [Cowgod's Chip-8 Technical Reference v1.0](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM), this instruction is defined as:

>*1nnn - JP addr*
>
>Jump to location nnn.
>
>The interpreter sets the program counter to nnn.

so it is like this funtion was:

`move_program_counter(x) -> program_counter = x`


Now we know we need to extract arguments of the instruction, the nnn, the last three digits:

**Last three hex digits (NNN)**  

`0x13A5 & 0x0FFF = 3A5`

We then set the program counter to 0x3A5.

That is it, your first instruction.


---

## Instruction: 1NNN (Jump)

**Behavior:**


PC = NNN


This overrides normal sequential execution.

Important detail:

- The current value of PC is irrelevant, as you will replace it.
- Be sure that the increment of +2 happened before the decode step



---

## Instruction: 6XNN (Set Register)


**Behavior:**

This instruction is used to assign a value to a register.

You need to extract X and NN from the instruction, check `chk02-extracting-opcode-values.md` if you are having trouble with the bit extractions.

X is the register indicator

NN is the value to assign to it, overwrite:

VX = NN

Remember: Registers are 8-bit.  
The final values must stay between 0 and 255.

Right now it is impossible to assign a value higher than 255 (FF in hex), but later it could happen.

---


## Instruction: BNNN (Jump with V0 Offset)


**Behavior:**

The program counter is set to the address `nnn` plus the value stored in register `V0`.

This instruction behaves like a normal jump, but the final destination is offset by the value of `V0`. It is commonly used to implement simple jump tables or position-dependent control flow.

Execution:

PC = nnn + V0

Notes:

- `V0` is always used as the offset register.
- The jump replaces the normal program counter progression.
- No additional registers or flags are modified.


## Minimal Execution Loop

You can now build *the* real loop:


        loop:
                fetch instruction
                increment PC by 2
                decode instruction
                execute behavior

                                
Hint:

If an instruction is not implemented:

- Print an error and Stop execution
- Print a warning that instruction XYZ is not implemented

Silent failure makes debugging significantly harder.

---

## Validation

Use the `rom_loading_test.ch8` again to check that:


- It set registers
- Loops infinitely


Registers 0 to 3 are loaded with values:
- V0 = 2
- V1 = 11
- V2 = 12
- V3 = 13

No other register is set!

Program counter keeps returning to the beggining


---

## Common Mistakes

- Forgetting that PC already incremented
- Modifying PC incorrectly during jump
- Dispatching only by first nibble without validating full opcode pattern
- Ignoring unknown instructions silently


---

## Checkpoint Complete When

- Instructions are decoded reliably
- `1NNN` correctly changes PC
- `6XNN` correctly modifies registers
- Execution loop runs without crashing
- Unknown opcodes are detected explicitly

At this point, you have built a minimal programmable virtual machine.
