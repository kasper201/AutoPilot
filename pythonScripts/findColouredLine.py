# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Find Lines Example
#
# This example shows off how to find lines in the image. For each line object
# found in the image a line object is returned which includes the line's rotation.

# Note: Line detection is done by using the Hough Transform:
# http://en.wikipedia.org/wiki/Hough_transform
# Please read about it above for more information on what `theta` and `rho` are.

# find_lines() finds infinite length lines. Use find_line_segments() to find non-infinite lines.

import sensor
import time

ENABLE_LENS_CORR = False  # turn on for straighter lines...

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # grayscale is faster
sensor.set_framesize(sensor.HVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

def RGB_2_HSV(RGB):
    ''' Converts an integer RGB tuple (value range from 0 to 255) to an HSV tuple '''

    # Unpack the tuple for readability
    R, G, B = RGB

    # Compute the H value by finding the maximum of the RGB values
    RGB_Max = max(RGB)
    RGB_Min = min(RGB)

    # Compute the value
    V = RGB_Max;
    if V == 0:
        H = S = 0
        return (H,S,V)


    # Compute the saturation value
    S = 255 * (RGB_Max - RGB_Min) // V

    if S == 0:
        H = 0
        return (H, S, V)

    # Compute the Hue
    if RGB_Max == R:
        H = 0 + 43*(G - B)//(RGB_Max - RGB_Min)
    elif RGB_Max == G:
        H = 85 + 43*(B - R)//(RGB_Max - RGB_Min)
    else: # RGB_MAX == B
        H = 171 + 43*(R - G)//(RGB_Max - RGB_Min)

    return (H, S, V)


# All line objects have a `theta()` method to get their rotation angle in degrees.
# You can filter lines based on their rotation angle.

#min_degree = 0
#max_degree = 179

# All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points
# and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

while True:
    clock.tick()
    img = sensor.snapshot()
    if ENABLE_LENS_CORR:
        img.lens_corr(1.8)  # for 2.8mm lens...

    for l in img.find_lines(threshold=1000, theta_margin=25, rho_margin=25):
        #if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            # Get the colour rgb from line
            startPixel = img.get_pixel(l.x1(), l.y1())
            endPixel = img.get_pixel(l.x2(), l.y2())

            # Convert to hsv
            startHSV = RGB_2_HSV(startPixel)
            endHSV = RGB_2_HSV(endPixel)

            # Check if h is blue
            if (140 <= startHSV[0] <= 260) and (140 <= endHSV[0] <= 260):
                # Draw a red line
                img.draw_line(l.line(), color=(255, 0, 0))

    #print("FPS %f" % clock.fps())
    print(startHSV)


# About negative rho values:
#
# A [theta+0:-rho] tuple is the same as [theta+180:+rho].
