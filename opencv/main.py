import requests
import time
import numpy as np
import cv2
import os
import sys, getopt
import signal
#from edge_impulse_linux.image import ImageImpulseRunner

# Nicla server address
server_address = "http://192.168.90.29:8080/"
count = 0

# Create a session object to reuse connections
session = requests.Session()

# Edge Impulse specifics
runner = None
#dir_path = os.path.dirname(os.path.realpath(_file_))
#modelfile = "modelfileV3.eim" 
#model = "modelfileV3.eim"

# if you don't want to see a camera preview, set this to False
show_camera = True
#if (sys.platform == 'linux' and not os.environ.get('DISPLAY')):
 #S   show_camera = False
# Define the regions of interest (ROIs)
roiFront = (60, 60, 340, 5)
roiBack = (100, 112, 240, 5)
rightRoiBack = (240, 112, 120, 5)
leftRoiBack = (100, 112, 180, 5)

roiLineBack = (0, 60, 480, 5)
roiLineFront = (0, 15, 480, 5)

roiLine = (60, 5, 340, 50)

roiRight = (240, 5, 150, 5)



def find_first_white_pixel_right(img, roi):
    roi_img = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    white_pixels_count = cv2.countNonZero(roi_img)
    
    if white_pixels_count > 25:
        for x in range(roi_img.shape[1] - 1, -1, -1):
            if roi_img[0, x] == 255:
                return x + roi[0]
    return -1

def find_first_white_pixel_left(img, roi):
    roi_img = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    white_pixels_count = cv2.countNonZero(roi_img)
    
    if white_pixels_count > 25:
        for x in range(roi_img.shape[1]):
            if roi_img[0, x] == 255:
                return x + roi[0]
    return -1

# Function to count white pixels in an ROI
def count_white_pixels(img, roi, pattern_name):
    roi_img = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    mean_value = cv2.mean(roi_img)[0]
    # For manual figuring out the value
    print(f"{pattern_name} mean ROI {roi}: {mean_value}")
    # Threshold for enough white pixels from line
    return mean_value >= 130

def count_white_pixelsBack(img, roi, pattern_name):
    roi_img = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    mean_value = cv2.mean(roi_img)[0]
    # For manual figuring out the value
    print(f"{pattern_name} mean ROI {roi}: {mean_value}")
    # Threshold for enough white pixels from line
    return mean_value >= 106

def countDistance(img):

    frame = img[roiLine[1]:roiLine[1]+roiLine[3], roiLine[0]:roiLine[0]+roiLine[2]]
    # Apply Canny edge detection
    edges = cv2.Canny(frame, 50, 150)
    
    # Apply a region of interest mask to focus on the road
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, [np.array([(0, 185), (frame.shape[1], 185), (frame.shape[1], 0), (0, 0)])], 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    
    # Apply Hough transform to detect lines
    lines = cv2.HoughLinesP(masked_edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=30, maxLineGap=100)
    
    # Initialize variables to store information about the road
    left_lane_lines = []
    right_lane_lines = []
    
    # Filter lines into left and right lanes based on slope
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1 + 1e-6)  # Adding a small value to avoid division by zero
            if abs(slope) < 0.5:  # Ignore lines with a slope less than 0.5 to avoid horizontal lines
                continue
            if slope < 0:
                left_lane_lines.append(line)
            elif slope > 0:
                right_lane_lines.append(line)

    # Determine the car position relative to the lanes
    if len(left_lane_lines) > 0 and len(right_lane_lines) > 0:
        # Calculate the midpoint of the lanes
        left_x = int(np.mean([line[0][0] for line in left_lane_lines]))
        right_x = int(np.mean([line[0][2] for line in right_lane_lines]))
        road_center = (left_x + right_x) // 2
        frame_center = frame.shape[1] // 2
        
        print("frame center: ", frame_center)
        print("road center: ", road_center)
        return (2*(frame_center-road_center))+100 
    else:
       	return 100
    print("Road Not Detected")



# Function to send command
def send_command(command):
    response = session.get(server_address, params={"command": command})
    print("Sent command:", command)
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        
        if 'image' in content_type:
            print("Response is an image")
            image_data = response.content
            # Decode image data
            image_np = np.frombuffer(image_data, dtype=np.uint8)
            image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            imageDetection(image)
            countDistance(image)
            # Display the image in a window
            cv2.imshow('Image', image)
            cv2.waitKey(1)
            #return image_data
        else:
            print("Response body:", response.text)
    else:
        print("Error:", response.status_code)


def getDirection(img):
    right1 = find_first_white_pixel_right(img, roiLineFront)
    right2 = find_first_white_pixel_right(img, roiLineBack)
    left1 = find_first_white_pixel_left(img, roiLineFront)
    left2 = find_first_white_pixel_left(img, roiLineBack)
    average1 = round((left1 + right1) / 2)
    average2 = round((left2 + right2) / 2) + 19
    print(f"average1: {average1}, average2: {average2}" )

    us_average = average2 - 240
    if us_average < 30 and us_average > -30:
        calc = round((us_average / 3) * -1)
    else:
        calc = round((us_average / 5) * -1)

    if calc > 15:
        calc = 15
    elif calc < -20:
        calc = -20

    if calc > -4 and calc < 4:
        calc = 0
    
    return  calc + 100

def getDirectionOld(img):
    right1 = find_first_white_pixel_right(img, roiLineFront)
    right2 = find_first_white_pixel_right(img, roiLineBack)
    left1 = find_first_white_pixel_left(img, roiLineFront)
    left2 = find_first_white_pixel_left(img, roiLineBack)
    rightDif = right1 - right2
    leftDif = left1 - left2
    print(f"right1: {right1}, right2: {right2}, left1: {left1}, left2: {left2}")
    return round(rightDif - leftDif - 80) #number between 100 and -100

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

def center(bin):
    return countDistance(bin)

def help():
    print('python classify-image.py <path_to_model.eim>')

def imageDetection(img):
    #integrste back
    # Line detection
    # Image processing
    cropped_img = img[:160, :]
    gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray_img, 101, 255, cv2.THRESH_BINARY_INV)

    if straightLine(binary_img):
        print("Straight line")
    elif leftTurn(binary_img):
        print("Left turn")
    elif rightTurn(binary_img):
         print("Right turn")
    elif intersection(binary_img):
         print("Intersection")
    else:
         print("Unknown")

    # center(gray_img)
    speed = 120
    turn = getDirection(binary_img)#center(gray_img)
    control = speed * 200 + turn
    command = "Integer=" + str(control)
    send_command(command)
    time.sleep(0.2)
    cv2.rectangle(cropped_img, (roiLineFront[0], roiLineFront[1]), (roiLineFront[0] + roiLineFront[2], roiLineFront[1] + roiLineFront[3]), (0, 255, 0), 2)
    cv2.rectangle(cropped_img, (roiLineBack[0], roiLineBack[1]), (roiLineBack[0] + roiLineBack[2], roiLineBack[1] + roiLineBack[3]), (255, 0, 0), 2)
    cv2.imshow('Image', cropped_img)
    # the image will be resized and cropped, save a copy of the picture here
    # so you can see what's being passed into the classifier
    #cv2.imwrite('debug.jpg', cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR))

        

def main(argv):
    
    print('debug')

    #model = args[0]


	# Main loop communication
    # Get user input for the command
    
    # this is where the send function was originally placed

    #dir_path = os.path.dirname(os.path.realpath(_file_))
    #modelfile = os.path.join(dir_path, model)

    #print('MODEL: ' + modelfile)
    while True:
        # Send the command
        send_command("VISION")
        time.sleep(0.2)

if __name__ == "__main__":
    main(sys.argv[1:])
