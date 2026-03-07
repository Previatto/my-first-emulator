# Checkpoint 08 – Timers and Sound

## Objective

Implement the delay and sound timers operating at **60 Hz**.

This stage introduces time-based behavior independent of CPU execution speed.

---

## CHIP-8 Timer Model

CHIP-8 defines two timers:

- **Delay timer**
- **Sound timer**

Both timers:

- Store an **8-bit value**
- Decrement at **60 times per second**
- Stop automatically when reaching **0**

Example:

If the timer is set to `60`, it will take **1 second** to reach zero.

Timers are not affected by instruction speed. Even if your CPU runs faster or slower, timers must still tick exactly 60 times per second.

---

# Instructions to Implement

## FX07 – Read Delay Timer

Behavior:


VX = delay_timer


This instruction simply copies the current delay timer value into a register.

No modification to the timer itself occurs.

---

## FX15 – Set Delay Timer

Behavior:


delay_timer = VX


The delay timer begins decrementing at the next timer update tick.

---

## FX18 – Set Sound Timer

Behavior:


sound_timer = VX


While the sound timer is greater than zero, a tone should be emitted.

When the timer reaches zero, the sound must stop.

---

# Timing Requirement

Timers must decrement at exactly:


60 Hz


Meaning:


1 decrement every 1/60 second
≈ 16.67 milliseconds


Timers must **not** depend on the speed of your instruction loop.

If your emulator executes instructions faster or slower, timers must still behave consistently.

---

# Recommended Implementation Strategy

Track real elapsed time.

Typical model:


last_timer_update = current_time()


During each emulator cycle:


if (current_time - last_timer_update) >= 1/60 second:
decrement timers
last_timer_update = current_time


Timer decrement rule:


if delay_timer > 0:
delay_timer -= 1

if sound_timer > 0:
sound_timer -= 1


Never allow timers to go below zero.

---

# Sound Behavior

When:


sound_timer > 0


A tone should play.

When:


sound_timer == 0


Sound should stop.

The exact tone frequency is not critical. Most implementations simply play a continuous beep.

The important property is **duration accuracy**, not audio fidelity.

---

# Validation Strategy

## Delay Timer Test

Create a ROM that:

1. Sets `delay_timer = 60`
2. Reads timer repeatedly

Expected behavior:

- Timer decreases gradually
- Reaches zero after ~1 second

If it finishes instantly, timers are tied to CPU speed.

---

## Sound Timer Test

Set:


sound_timer = 30


Expected:

- Tone plays for approximately **0.5 seconds**
- Sound stops automatically

---

## Boundary Test

Set:


delay_timer = 1


Expected:

- Decrement to zero
- Remain at zero

Timers must **never become negative**.

---

# Common Mistakes

- Decrementing timers every instruction cycle
- Running timers faster than 60 Hz
- Allowing timers to become negative
- Forgetting to stop sound when timer reaches zero
- Tying timers to frame rendering instead of real elapsed time

---

# Checkpoint Completion Criteria

You are complete when:

- Delay timer decrements at approximately **60 Hz**
- Sound timer decrements at approximately **60 Hz**
- Both timers stop exactly at **0**
- Sound plays only while `sound_timer > 0`
- Timers behave consistently regardless of CPU speed

At this stage, your emulator now supports:

- Control flow
- Arithmetic operations
- Graphics rendering
- Input handling
- Real-time timers
- Audio signaling

Your emulator is now capable of running most classic CHIP-8 programs.
