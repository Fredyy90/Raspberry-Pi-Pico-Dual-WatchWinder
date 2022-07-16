# Raspberry Pi Pico - Watch Winder Code
# Software Setup:
#   Adafruit CircuitPython 7
#
# Hardware setup:
#   Stepper1: 28BYJ-48 Stepper Motor via ULN2803 driver breakout on GP2, GP3, GP4, GP5
#   Stepper2: 28BYJ-48 Stepper Motor via ULN2803 driver breakout on GP6, GP7, GP8, GP9
#   external power supply
#   Button on GP10 and ground

import time
import board
from winder import Winder
from digitalio import DigitalInOut, Direction, Pull

print("Raspberry Pi Pico - Watch Winder")

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

last_rotation = 0  # time of last_rotation
rotation_offset = 60  # time between rotations

# Mode button setup
button = DigitalInOut(board.GP10)
button.direction = Direction.INPUT
button.pull = Pull.UP

#
W1_coils = (
    DigitalInOut(board.GP2),  # Motor1 - A1
    DigitalInOut(board.GP3),  # Motor1 - A2
    DigitalInOut(board.GP4),  # Motor1 - B1
    DigitalInOut(board.GP5),  # Motor1 - B2
)
W2_coils = (
    DigitalInOut(board.GP6),  # Motor2 - A1
    DigitalInOut(board.GP7),  # Motor2 - A2
    DigitalInOut(board.GP8),  # Motor2 - B1
    DigitalInOut(board.GP9),  # Motor2 - B2
)

winder1 = Winder(W1_coils)
winder2 = Winder(W2_coils)


def blink(times):
    for _ in range(times):
        led.value = False
        time.sleep(0.1)
        led.value = True
        time.sleep(0.1)


while True:

    if (winder1.update() & winder2.update()) == True:  # update both winders and if we did a step trigger a delay
        winder1.waitAfterStep()

    if not button.value:
        blink(2)
        winder1.addRotation()
        winder2.addRotation()
        time.sleep(0.8)  # big debounce

    if (time.time() - last_rotation > rotation_offset):  # add new steps every `rotation_offset` seconds
        print("Added new Rotation")
        last_rotation = time.time()
        winder1.addRotation(direction = Winder.RANDOM, count = 2)
        winder2.addRotation(direction = Winder.RANDOM, count = 2)
