import sensor, image, time

# Initialize the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# Defining the regions of interest (ROIs)
roi1 = (0, 0, 80, 60)
roi2 = (80, 0, 80, 60)
roi3 = (0, 60, 80, 60)
roi4 = (80, 60, 80, 60)

# Load template.
# Template should be a small (eg. 32x32 pixels) grayscale image.
temp1 = image.Image("/tem1.jpg").to_grayscale()
temp2 = image.Image("/tem2.jpg").to_grayscale()
temp3 = image.Image("/tem3.jpg").to_grayscale()
temp4 = image.Image("/tem4.jpg").to_grayscale()

def detect_intersection():

    # Check for the template in each ROI
    if (img.find_template(temp1, 0.7, roi=roi1) and
        img.find_template(temp2, 0.7, roi=roi2) and
        img.find_template(temp3, 0.7, roi=roi3) and
        img.find_template(temp4, 0.7, roi=roi4)):
        return True
    else:
        return False

while True:
    clock.tick()
    img = sensor.snapshot()

    # Draw the ROIs on the frame buffer
    img.draw_rectangle(roi1, color=(255, 0, 0))  # Red
    img.draw_rectangle(roi2, color=(0, 0, 255))  # Blue
    img.draw_rectangle(roi3, color=(255, 255, 0))  # Yellow
    img.draw_rectangle(roi4, color=(0, 255, 0))  # Green

    img = img.to_grayscale()
    img = img.binary([(18, 0)])

    if detect_intersection():
        print("Intersection detected!")
    else:
        print("No intersection detected!")
