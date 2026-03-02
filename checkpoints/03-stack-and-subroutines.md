Checkpoint 03 – Stack and Subroutines

Objective
Implement subroutine calls and returns using a stack.

You are now adding controlled control-flow, not just jumps.

What You Should Already Have

Working memory

Working PC

Working fetch–decode–execute loop

16 registers

Jump instruction (1NNN)

Now you will implement:

2NNN (call subroutine)

00EE (return from subroutine)

A functioning stack

What Is a Subroutine?

A subroutine is a reusable block of code.

When you “call” a subroutine:

Save the current execution location.

Jump to another address.

Execute code there.

Return to the original location.

The stack exists to remember where to return.

What You Need to Implement

Stack

Maximum depth: 16 levels

Stores return addresses

You may optionally track a stack pointer

Instruction: 2NNN (Call)

Behavior:

Push current PC onto the stack.
Set PC = NNN.

Important detail:

Because PC was already incremented after fetch, the value you push must be the correct return address (the next instruction to execute after return).

Instruction: 00EE (Return)

Behavior:

Pop address from stack.
Set PC to that address.

Mental Model

Main program at 0x200:

200: 220A ; Call subroutine at 0x20A
202: 6001 ; Continue here after return

Subroutine:

20A: 6005
20C: 00EE ; Return

Execution flow:

Push 0x202

Jump to 0x20A

Execute subroutine

Pop 0x202

Resume execution

Validation

Create a small test ROM:

Set a register inside subroutine

Return

Confirm execution continues correctly

Test nested calls if possible.

Common Mistakes

Forgetting PC was already incremented

Pushing incorrect return address

Stack overflow (more than 16 calls)

Stack underflow (return without call)

Not handling invalid return gracefully

Do not silently ignore stack errors. Print an error and stop execution.

Checkpoint Complete When

2NNN correctly pushes and jumps

00EE correctly restores PC

Nested calls work

Stack never exceeds 16 levels

Return resumes exactly where expected

You now have structured control flow.