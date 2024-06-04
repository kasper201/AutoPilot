import sensor, image, time

# Initialize the sensor and set up the camera
sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # grayscale is faster
sensor.set_framesize(sensor.HVGA)
sensor.skip_frames(time=2000)

clock = time.clock()

# Define the regions of interest (ROIs), seen from human perspective on buffer
roiFront = (60, 60, 340, 5)
roiBack = (100, 112, 240, 5)
rightRoiBack = (240, 112, 120, 5)
leftRoiBack = (100, 112, 180, 5)

# Function to count white pixels in an ROI
def count_white_pixels(img, roi, pattern_name):
    mean_value = img.get_statistics(roi=roi).mean()
    # For manual figuring out the value
    print(f"{pattern_name} mean ROI {roi}: {mean_value}")
    # Threshold for enough white pixels from line
    return mean_value >= 130

def count_white_pixelsBack(img, roi, pattern_name):
    mean_value = img.get_statistics(roi=roi).mean()
    # For manual figuring out the value
    print(f"{pattern_name} mean ROI {roi}: {mean_value}")
    # Threshold for enough white pixels from line
    return mean_value >= 106

# Functions for detecting each pattern
def straightLine(img):
    if count_white_pixels(img, roiFront, "Straight line") and count_white_pixels(img, roiBack, "Straight line"):
        return True
    return False

def intersection(img):
    if count_white_pixels(img, roiFront, "Intersection") and not count_white_pixelsBack(img, roiBack, "Intersection"):
        return True
    return False

def leftTurn(img):
    if count_white_pixels(img, roiFront, "Left turn") and count_white_pixelsBack(img, leftRoiBack, "Left turn"):
        return True
    return False

def rightTurn(img):
    if count_white_pixels(img, roiFront, "Right turn") and count_white_pixelsBack(img, rightRoiBack, "Right turn"):
        return True
    return False

while True:
    clock.tick()
    img = sensor.snapshot()

    # Draw for easier debugging
    img.draw_rectangle(roiFront, color=(255, 0, 0))  #Red
    img.draw_rectangle(roiBack, color=(0, 0, 255))  # Blue
    img.draw_rectangle(leftRoiBack, color=(255, 255, 0))  # Yellow
    img.draw_rectangle(rightRoiBack, color=(0, 255, 0))  # Green

    img = img.to_grayscale()
    img = img.binary([(101, 20)])

    # Road type detection
    if straightLine(img):
        print("Straight line")
    elif leftTurn(img):
        print("Left turn")
    elif rightTurn(img):
        print("Right turn")
    elif intersection(img):
        print("Intersection")
    else:
        print("Unknown")
