# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor
import time
import pyb
from machine import Pin

# define the communication pins to the zumo
fromZumo = Pin("PA10", Pin.IN)
toZumo = Pin("PA9", Pin.OUT_PP)
toZumo.high() # start with toZumo high

def converter(nr): # convert number to signal
    global toZumo # Declare toZumo again to make sure its using the global variable
    #print(nr)
    #if nr < 0:
    #       nr = ((-nr) ^ 0xFF) + 1  # Two's complement conversion
    waarde = nr & 0b11111111
    print(waarde)
    i = 0
    tmp = waarde
    while i < 8:
        print(f"{tmp:08b}")
        print("gewoon doen", waarde)
        tmp = tmp & 0b1
        print(tmp)
        if (tmp):
            toZumo.high()
        else:
            toZumo.low()
        pyb.delay(5)
        i += 1
        waarde = waarde >> 1
        tmp = waarde

# the sendToZumo function converts speed and turn to a signal for the zumo to pick up
# speed is 100 to -100 and turn is 100 to -100
def sendToZumo(speed, turn):
    if (speed > 100 or speed < -100 or turn > 100 or turn < -100):
        print("Illegal value entered! Value must stay between -100 and 100")
    print("sending to zumo")
    global toZumo
    toZumo.low() # set start bit
    pyb.delay(5)
    converter(speed)
    toZumo.high()
    pyb.delay(2000)
    toZumo.low() # set start bit
    pyb.delay(5)
    converter(turn)
    toZumo.high()
    pyb.delay(2000)

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.
sensor.set_vflip(True)
#sensor.set_lens_correction(True, 200, 20)
sensor.ioctl(sensor.IOCTL_SET_FOV_WIDE, True)

while True:
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot()  # Take a picture and return the image.
    print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
    sendToZumo(31, 6)

