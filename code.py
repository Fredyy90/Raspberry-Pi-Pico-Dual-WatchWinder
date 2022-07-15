# SPDX-FileCopyrightText: 2021 jedgarpark for Adafruit Industries
# SPDX-License-Identifier: MIT

# Pico stepper demo
# Hardware setup:
#    Stepper motor via DRV8833 driver breakout on GP21, GP20, GP19, GP18
#   external power supply
#   Button on GP3 and ground

import time
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import stepper

print("Stepper test")

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True


def blink(times):
    for _ in range(times):
        led.value = False
        time.sleep(0.1)
        led.value = True
        time.sleep(0.1)


# Mode button setup
button = DigitalInOut(board.GP10)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Stepper motor setup
DELAY = 0.005  # fastest is ~ 0.004, 0.01 is still very smooth, gets steppy after that
STEPS = 2048  # this is a full 360º
coilsM1 = (
    DigitalInOut(board.GP2),  # A1
    DigitalInOut(board.GP3),  # A2
    DigitalInOut(board.GP4),  # B1
    DigitalInOut(board.GP5),  # B2
)
coilsM2 = (
    DigitalInOut(board.GP6),  # A1
    DigitalInOut(board.GP7),  # A2
    DigitalInOut(board.GP8),  # B1
    DigitalInOut(board.GP9),  # B2
)
for coil in coilsM1 + coilsM2:
    coil.direction = Direction.OUTPUT
stepper_motor1 = stepper.StepperMotor(
    coilsM1[0], coilsM1[1], coilsM1[2], coilsM1[3], microsteps=None
)
stepper_motor2 = stepper.StepperMotor(
    coilsM2[0], coilsM2[1], coilsM2[2], coilsM2[3], microsteps=None
)
M1_steps = 0
M2_steps = 0


def step():
    global M1_steps
    global M2_steps

    if M1_steps > 0:
        stepper_motor1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        M1_steps -= 1
    if M1_steps < 0:
        stepper_motor1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        M1_steps += 1
    if M2_steps > 0:
        stepper_motor2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        M2_steps -= 1
    if M2_steps < 0:
        stepper_motor2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        M2_steps += 1
    time.sleep(DELAY)


while True:

    if M1_steps != 0 or M2_steps != 0:
        print(M1_steps)
        step()
    else:
        stepper_motor1.release()
        stepper_motor2.release()

    if not button.value:
        blink(2)
        M1_steps += STEPS
        M2_steps += STEPS
        time.sleep(0.8)  # big debounce
