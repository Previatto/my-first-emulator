import math
import tkinter as tk
from array import array
from tkinter import filedialog

import pygame

import chip8

pixel_color = pygame.Color("green1")
key_lookup = {
    pygame.K_1: 0,
    pygame.K_2: 1,
    pygame.K_3: 2,
    pygame.K_4: 3,
    pygame.K_q: 4,
    pygame.K_w: 5,
    pygame.K_e: 6,
    pygame.K_r: 7,
    pygame.K_a: 8,
    pygame.K_s: 9,
    pygame.K_d: 10,
    pygame.K_f: 11,
    pygame.K_z: 12,
    pygame.K_x: 13,
    pygame.K_c: 14,
    pygame.K_v: 15,
}


def generate_square_wave(frequency=500, amplitude=16000, sample_rate=44100):
    samples = array("h")  # signed 16-bit integers

    period = sample_rate / frequency
    half_period = period / 2

    for i in range(int(period)):
        if (i % period) < half_period:
            samples.append(amplitude)  # positive amplitude
        else:
            samples.append(-amplitude)  # negative amplitude

    return pygame.mixer.Sound(buffer=samples)


emul = chip8.chip8()
# emul.info()
emul.warmup()


# open-file dialog
root = tk.Tk()
root.withdraw()  # hides the main window

root.attributes("-topmost", True)
root.update()  # ensures attribute is applied
filename = filedialog.askopenfilename(
    title="Select a ROM...",
    filetypes=[("CHIP-8 ROMs", "*.ch8 *.rom"), ("All files", "*.*")],
)
root.destroy()

# pygame setup
pygame.mixer.pre_init(22050, -16, 1, 512)
pygame.init()

buzzer_sound = generate_square_wave(frequency=550, amplitude=6000, sample_rate=22050)
buzzer_channel = None

screen = pygame.display.set_mode((64 * 10, 32 * 10))
# surface = screen.get_surface()
clock = pygame.time.Clock()
running = True

emul.load_rom(filename)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            for k in key_lookup.keys():
                if event.key == k:
                    emul.keys[key_lookup[k]] = True
        if event.type == pygame.KEYUP:
            for k in key_lookup.keys():
                if event.key == k:
                    emul.keys[key_lookup[k]] = False

    screen.fill("black")
    for row in range(32):
        for column in range(64):
            if emul.screen[row][column] == 1:
                pygame.draw.rect(
                    screen, pixel_color, pygame.Rect(column * 10, row * 10, 10, 10)
                )

    if emul.timer_sound > 0:
        if buzzer_channel is None or not buzzer_channel.get_busy():
            buzzer_channel = buzzer_sound.play(-1)  # loop forever
    else:
        if buzzer_channel is not None:
            buzzer_channel.stop()
            buzzer_channel = None

    emul.loop()
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
