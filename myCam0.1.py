# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor
import time
import image
from machine import Pin


fromZumo = Pin("PA10", Pin.IN)
toZumo = Pin("PA9", Pin.OUT_PP)

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.HVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.
sensor.set_vflip(True)
#sensor.set_lens_correction(True, 200, 20)
sensor.ioctl(sensor.IOCTL_SET_FOV_WIDE, True)
face_cascade = image.HaarCascade("frontalface", stages=25)
faceImage = image.Image("test.jpg", copy_to_fb=False)

while True:
    clock.tick()  # Update the FPS clock.
    img = sensor.snapshot()  # Take a picture and return the image.
    print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
    img = sensor.snapshot()  # Take a picture and return the image.
    print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
    # to the IDE. The FPS should increase once disconnected.
    # face recognition time
    # Find objects.

    # Note: Lower scale factor scales-down the image more and detects smaller objects.

    # Higher threshold results in a higher detection rate, with more false positives.
    boundingBoxes = img.find_features(face_cascade, threshold=1, scale_factor=1.5)

    # Draw objects

    for boundingBox in boundingBoxes:

        faceX = boundingBox[0]

        faceY = boundingBox[1]

        faceWidth = boundingBox[2]


        # Calculates the scale ratio to scale the bitmap image to match the bounding box

        scale_ratio = faceWidth / faceImage.width()

        # Draws the bitmap on top of the camera stream

        img.draw_image(faceImage, faceX, faceY, x_scale=scale_ratio, y_scale=scale_ratio)


