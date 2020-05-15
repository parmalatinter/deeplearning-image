#!/usr/bin/env python

import time
import grovepi
import children.grove_tilt_sensor as tilt
import children.grove_buzzer as buzzer
import children.grove_led as led
import children.grove_button as button

class TiltWarning:

    def __init__(self, pin_tilt_sensor, pin_buzzer, pin_led, pin_button):
        self.tilt_sensor = tilt.TiltSensor(pin_tilt_sensor)
        self.buzzer = buzzer.Buzzer(pin_buzzer)
        self.led = led.Led(pin_led)
        self.button = button.Button(pin_button)
        self.enable = True
        self.buzzer.play()
        time.sleep(.5)
        self.buzzer.stop()

    def play(self):
        
        while True:
            try:
                is_on = self.button.check()
                is_open = self.tilt_sensor.check()
                print("is_on", is_on)
                print("is_open", is_open)
                print("self.enable", self.enable)
                if (is_on == True):                   
                    if (self.enable == True):
                        self.enable = False
                        self.buzzer.play()
                        time.sleep(.5)
                        self.buzzer.stop()
                        time.sleep(.5)
                        self.buzzer.play()
                        time.sleep(.5)
                        self.buzzer.stop()
                        print('off')
                        
                    else:
                        self.enable = True
                        self.buzzer.play()
                        time.sleep(.5)
                        self.buzzer.stop()
                        print('on')
                        

                if (is_open == True and self.enable == True):
                    self.buzzer.play()
                    self.led.play()
                    time.sleep(.5)
                    self.buzzer.stop()
                    self.led.stop()
                    print('open')

            except IOError:
                print("Error")


if __name__ == '__main__':
    pin_tilt_sensor = 3
    pin_buzzer = 7
    pin_led = 5
    pin_button = 6
    tiltWarning = TiltWarning(pin_tilt_sensor, pin_buzzer, pin_led, pin_button)
    tiltWarning.play()
