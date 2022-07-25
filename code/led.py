from micropython import const
from digitalio import DigitalInOut, Direction, Pull
from adafruit_ticks import ticks_ms, ticks_less, ticks_add


_blink_delay = const(200)

class LED:

    blinks = 0
    next_change = ticks_ms()

    def __init__(self, led_pin) -> None:

        self.pin = DigitalInOut(led_pin)
        self.pin.direction = Direction.OUTPUT
        self.pin.value = False

    def update(self) -> None:

        if ticks_less(self.next_change, ticks_ms()):

            self.next_change = ticks_add(self.next_change, _blink_delay)

            if (self.blinks > 0 and self.pin.value == False):
                self.blinks -= 1
                self.pin.value = True
            elif (self.pin.value == True):
                self.pin.value = False

    def addBlinks(self, blinks) -> None:
        self.blinks += blinks
