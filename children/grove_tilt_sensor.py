#!/usr/bin/env python

import time
import grovepi


class TiltSensor():

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "INPUT")

    def check(self):
  
        try:
            val = grovepi.digitalRead(self.pin)
            print(val)
            if val == 0:
                return True

            time.sleep(.5)

        except IOError:
            print("Error")
            return False


if __name__ == '__main__':
    tiltSensor = TiltSensor(3)
    print(tiltSensor.check())
