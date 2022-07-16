import time
from random import random
from micropython import const
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import stepper



class Winder:

    stepsPerRotation = 2048
    stepsDelay = 0.002

    CWSteps = 0
    CCWSteps = 0

    FORWARD = const(1)
    BACKWARD = const(2)
    RANDOM = const(3)

    def __init__(self, coils) -> None:

        for coil in coils:
            coil.direction = Direction.OUTPUT

        self.stepper = stepper.StepperMotor(
            coils[0], coils[1], coils[2], coils[3], microsteps=None
        )

    def update(self) -> Boolean:

        if self.CWSteps > 0:
            self.stepper.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
            self.CWSteps -= 1
            return True

        if self.CCWSteps > 0:
            self.stepper.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
            self.CCWSteps -= 1
            return True

        if self.CWSteps <= 0 and self.CCWSteps <= 0:
            self.stepper.release()
            return False

    def waitAfterStep(self) -> None:
        time.sleep(self.stepsDelay)

    def addRotation(self, *, direction: int = RANDOM, count: int = 1) -> None:

        if direction == FORWARD:
            self.CWSteps += self.stepsPerRotation * count
        elif direction == BACKWARD:
            self.CCWSteps += self.stepsPerRotation * count
        elif direction == RANDOM:
            randomDir = random()
            if randomDir > 0.5:
                self.CWSteps += self.stepsPerRotation * count
                print("Added " + str(count) + " Roations -> CW")
            else:
                self.CCWSteps += self.stepsPerRotation * count
                print("Added " + str(count) + " Roations <- CCW")
