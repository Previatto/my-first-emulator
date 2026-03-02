Checkpoint 08 – Timers and Sound

Objective
Implement delay and sound timers operating at 60 Hz.

Overview

CHIP-8 includes:

Delay timer

Sound timer

Both decrement at 60 Hz until reaching zero.

These timers must operate independently of instruction speed.

Instructions to Implement

FX07 – VX = delay timer
FX15 – delay timer = VX
FX18 – sound timer = VX

Timing Requirement

Timers must decrement based on real elapsed time, not instruction cycles.

Recommended Approach

Track wall-clock time and reduce timer values every 1/60 second interval.

Sound Behavior

While sound timer > 0:
Emit a tone.

Tone accuracy is less important than duration correctness.

Validation

Set delay timer and observe decrement rate.

Confirm timer stops at zero.

Set sound timer and verify correct duration.

Common Mistakes

Tying timer decrement to CPU cycles.

Decrementing too quickly.

Negative timer values.

Sound playing continuously due to improper reset.