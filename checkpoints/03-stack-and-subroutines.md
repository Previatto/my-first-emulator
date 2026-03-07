# Checkpoint 03 – Stack and Subroutines

## Objective

Implement subroutine calls and returns using a stack.

You are now adding structured control flow — not just jumps.

---

## What You Should Already Have

Before starting this checkpoint, you should have:

- Working memory
- Working program counter (PC)
- Working fetch–decode–execute loop
- 16 general-purpose registers
- Working `1NNN` (jump instruction)
- Working `6XNN` (assign instruction)
- Working `BNNN` (jump with offset)

Now you will implement:

- `2NNN` (call subroutine)
- `00EE` (return from subroutine)
- Make sure you have a functioning stack

---

## What Is a Subroutine?

A subroutine is a reusable block of code.

When you call a subroutine:

1. Save the current execution location.
2. Jump to another address.
3. Execute code there.
4. Return to the original location.

The stack exists to remember where to return.

1. PC is at 0x204
2. Reads 2305
3. PC = PC + 2
4. Decode instruction 2305:
    5. Save PC position, 0x206, into stack, stack = [0x206]
    6. Move PC to 0x304
    7. Read and execute the instructions from then on...
8. In case a instruction 00EE is read, read the top of the stack, 0x206 in our example
9. Assign 0x206 to PC
10. Read and execute the instructions from then on...


Without a stack, you cannot safely nest subroutine calls.

---

## What You Need to Implement

### Stack

- Maximum depth: 16 levels
- Stores return addresses
- May use a stack pointer (optional but recommended)

The stack holds **addresses**, not instructions.

---

## Instruction: `2NNN` (Call Subroutine)

**Behavior:**

1. Push current PC onto the stack.
2. Set `PC = NNN`.

Important detail:

PC was already incremented during fetch.

Therefore, the value you push must be the correct return address: the next instruction to execute after the subroutine finishes.

If you push the wrong address, execution will resume incorrectly.

---

## Instruction: `00EE` (Return)

**Behavior:**

1. Pop address from stack.
2. Set `PC` to that address.

Do not increment PC again after returning.

You are restoring execution state exactly.

---

## Validation

Use the rom `subroutines.ch8`

Expected final state:

V0 = 0x01

V1 = 0x02

PC stuck at 0x202

Stack empty


I highly recommend that you print all your system variables (maybe not RAM) at each iteration, and make sure that:

200: 2208.  
Push 0x202
Jump to 0x208

208: 6001.  
V0 = 1

20A: 2210.  
Push 0x20C.  
Jump to 0x210

210: 6102.  
V1 = 2

212: 00EE.  
Pop → 0x20C

20C: 00EE.  
Pop → 0x202

202: 1202.  
Infinite loop


---

## Common Mistakes

- Forgetting PC was already incremented before call
- Pushing incorrect return address
- Stack overflow (more than 16 nested calls)
- Stack underflow (return without call)
- Incrementing PC after return incorrectly

Do not silently ignore stack errors.

If:

- Stack exceeds 16 levels → print error and stop
- Return occurs with empty stack → print error and stop

Silent corruption makes debugging extremely difficult.

---

## Checkpoint Complete When

- `2NNN` correctly pushes and jumps
- `00EE` correctly restores PC
- Nested calls work
- Stack never exceeds 16 levels
- Return resumes exactly where expected
- Stack errors are detected explicitly

At this point, you now have structured control flow.

Your emulator can execute reusable program logic.
