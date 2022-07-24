from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer

def setupButton(pin):
    button = DigitalInOut(pin)
    button.direction = Direction.INPUT
    button.pull = Pull.UP

    return Debouncer(button)
