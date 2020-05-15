#!/usr/bin/env python

import grovepi


class Led():

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "OUTPUT")

    def play(self):
        grovepi.digitalWrite(self.pin, 1)

    def stop(self):
        grovepi.digitalWrite(self.pin, 0)


if __name__ == '__main__':
    Led = Led(6)
    Led.play()
    Led.stop()
