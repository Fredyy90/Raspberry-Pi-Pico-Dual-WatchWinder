import time
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import stepper

class Winder:

    stepsPerRotation = 2048
    stepsDelay = 0.005

    CWSteps = 0
    CCWSteps = 0

    def __init__(self, coils):

        for coil in coils:
            coil.direction = Direction.OUTPUT

        self.stepper = stepper.StepperMotor(
            coils[0], coils[1], coils[2], coils[3], microsteps=None
        )

    def update(self):

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

    def waitAfterStep(self):
        time.sleep(self.stepsDelay)

    def addRotation(self):
        self.CWSteps += self.stepsPerRotation
