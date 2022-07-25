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
from functions import setupButton
from winder import Winder
from led import LED
from micropython import const
from digitalio import DigitalInOut, Direction

print("Raspberry Pi Pico - Watch Winder")

led = LED(board.LED)

last_rotation = 0                            # time of last_rotation
_rotation_timeinterval_offset = const(60*5)  # time between rotations | Default Value: 60*5 | 5 Minutes/300 Seconds
_rotation_per_timeinterval = const(3)        # rotations per timeinterval | Default value: 3
_turbo_button_rotation_amount = const(200)   # roations to add to a winder, when turbo button pressed | Default Value: 200

# button setup
buttons = {}
buttons["turboButtonW0"] = setupButton(board.GP10)
buttons["turboButtonW1"] = setupButton(board.GP11)
buttons["modeSwitchW0"] = setupButton(board.GP12)
buttons["modeSwitchW1"] = setupButton(board.GP13)

# winders setup
W0_coils = (
    DigitalInOut(board.GP2),  # Motor1 - A1
    DigitalInOut(board.GP3),  # Motor1 - A2
    DigitalInOut(board.GP4),  # Motor1 - B1
    DigitalInOut(board.GP5),  # Motor1 - B2
)
W1_coils = (
    DigitalInOut(board.GP6),  # Motor2 - A1
    DigitalInOut(board.GP7),  # Motor2 - A2
    DigitalInOut(board.GP8),  # Motor2 - B1
    DigitalInOut(board.GP9),  # Motor2 - B2
)

winders = []
winders.append(Winder(W0_coils))
winders.append(Winder(W1_coils))

while True:

    led.update()  # update led

    for button in buttons:  # update all buttons
        buttons[button].update()

    # update all winders
    winders[0].update()
    winders[1].update()

    if buttons["turboButtonW0"].rose:  # if turbo button for winder0 released, add multple rotations to winder.
        led.addBlinks(2)
        winders[0].addRotation(direction=Winder.RANDOM_SPLIT, count=_turbo_button_rotation_amount)

    if buttons["turboButtonW1"].rose:  # if turbo button for winder1 released, add multple rotations to winder.
        led.addBlinks(2)
        winders[1].addRotation(direction=Winder.RANDOM_SPLIT, count=_turbo_button_rotation_amount)

    if (abs(time.time() - last_rotation) > _rotation_timeinterval_offset):  # add new steps every `rotation_timeinterval_offset` seconds
        print(str(_rotation_timeinterval_offset)+" seconds elapsed, time to add "+str(_rotation_per_timeinterval)+" new rotations")
        last_rotation = time.time()

        if buttons["modeSwitchW0"].value is False:
            winders[0].addRotation(direction=Winder.RANDOM_SPLIT, count=_rotation_per_timeinterval)
        elif buttons["modeSwitchW1"].value is False:
            winders[1].addRotation(direction = Winder.RANDOM_SPLIT, count = _rotation_per_timeinterval)
        else:
            winders[0].addRotation(direction=Winder.RANDOM_SPLIT, count=_rotation_per_timeinterval)
            winders[1].addRotation(direction=Winder.RANDOM_SPLIT, count=_rotation_per_timeinterval)
