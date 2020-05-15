#!/usr/bin/env python

import time
import grovepi


class Button():

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "INPUT")

    def check(self):
        try:
            val = grovepi.digitalRead(self.pin)
            print(val)
            if val == 1:
                time.sleep(1)
            val = grovepi.digitalRead(self.pin)
            if val == 1:
                return True

            return False 

        except IOError:
            print("Error")
            return False


if __name__ == '__main__':
    button = Button(6)
    print(button.check())