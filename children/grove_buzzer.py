#!/usr/bin/env python

import grovepi


class Buzzer():

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "OUTPUT")

    def play(self):
        grovepi.digitalWrite(self.pin, 1)

    def stop(self):
        grovepi.digitalWrite(self.pin, 0)


if __name__ == '__main__':
    buzzer = Buzzer(6)
    buzzer.play()
    buzzer.stop()
