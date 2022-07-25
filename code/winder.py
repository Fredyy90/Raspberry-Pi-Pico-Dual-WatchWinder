from random import random
from micropython import const
from digitalio import Direction
from adafruit_ticks import ticks_ms, ticks_diff
from adafruit_motor import stepper


_stepsPerRotation = const(2048)
_stepsDelay = const(2)

class Winder:



    CWSteps = 0
    CCWSteps = 0

    last_step = ticks_ms()

    FORWARD = const(1)
    BACKWARD = const(2)
    RANDOM = const(3)
    RANDOM_SPLIT = const(4)

    def __init__(self, coils) -> None:

        for coil in coils:
            coil.direction = Direction.OUTPUT

        self.stepper = stepper.StepperMotor(
            coils[0], coils[1], coils[2], coils[3], microsteps=None
        )

    def update(self) -> bool:
        now = ticks_ms()
        if (ticks_diff(self.last_step, now) < _stepsDelay):

            self.last_step = now

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

    def addRotation(self, *, direction: int = RANDOM, count: int = 1) -> None:

        if direction == self.FORWARD:
            self.CWSteps += _stepsPerRotation * count
        elif direction == self.BACKWARD:
            self.CCWSteps += _stepsPerRotation * count
        elif direction == self.RANDOM:
            randomDir = random()
            if randomDir > 0.5:
                self.CWSteps += _stepsPerRotation * count
            else:
                self.CCWSteps += _stepsPerRotation * count
                print("Added " + str(count) + " Roations <- CCW")
        elif direction == self.RANDOM_SPLIT:
            cwRotations = round(count * random())
            self.CWSteps += _stepsPerRotation * cwRotations
            self.CCWSteps += _stepsPerRotation * (count - cwRotations)

