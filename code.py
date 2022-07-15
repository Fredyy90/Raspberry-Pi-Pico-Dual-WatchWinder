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
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import stepper

print("Stepper test")

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

last_rotation = 0;    # time of last_rotation
rotation_offset = 60; # time between rotations

# Mode button setup
button = DigitalInOut(board.GP10)
button.direction = Direction.INPUT
button.pull = Pull.UP

# Stepper motor setup
STEP_DELAY = 0.005  # fastest is ~ 0.004, 0.01 is still very smooth, gets steppy after that
STEPS = 2048        # this is a full 360º

M1_coils = (
    DigitalInOut(board.GP2),  # Motor1 - A1
    DigitalInOut(board.GP3),  # Motor1 - A2
    DigitalInOut(board.GP4),  # Motor1 - B1
    DigitalInOut(board.GP5),  # Motor1 - B2
)
M2_coils = (
    DigitalInOut(board.GP6),  # Motor2 - A1
    DigitalInOut(board.GP7),  # Motor2 - A2
    DigitalInOut(board.GP8),  # Motor2 - B1
    DigitalInOut(board.GP9),  # Motor2 - B2
)

for coil in M1_coils + M2_coils:
    coil.direction = Direction.OUTPUT

stepper_motor1 = stepper.StepperMotor(M1_coils[0], M1_coils[1], M1_coils[2], M1_coils[3], microsteps=None)
stepper_motor2 = stepper.StepperMotor(M2_coils[0], M2_coils[1], M2_coils[2], M2_coils[3], microsteps=None)
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
    time.sleep(STEP_DELAY)


def blink(times):
    for _ in range(times):
        led.value = False
        time.sleep(0.1)
        led.value = True
        time.sleep(0.1)


while True:

    if M1_steps != 0 or M2_steps != 0: #rotate if still steps queued
        print(M1_steps)
        step()
    else: #unpower stepper when not in used to save power and avoid heating up
        stepper_motor1.release()
        stepper_motor2.release()

    if not button.value:
        blink(2)
        M1_steps += STEPS
        M2_steps += STEPS
        time.sleep(0.8)  # big debounce

    if (time.time() - last_rotation > rotation_offset): #add new steps every `rotation_offset` seconds
        last_rotation = time.time()
        M1_steps += STEPS
        M2_steps += STEPS

