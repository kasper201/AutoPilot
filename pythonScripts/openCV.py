import requests
import time
import numpy as np
import cv2
import os
import sys, getopt
import signal
from edge_impulse_linux.image import ImageImpulseRunner

# Nicla server address
server_address = "http://192.168.90.29:8080/"
count = 0

# Create a session object to reuse connections
session = requests.Session()

# Edge Impulse specifics
runner = None
dir_path = os.path.dirname(os.path.realpath(__file__))
modelfile = "modelfileV3.eim" 
model = "modelfileV3.eim"

# if you don't want to see a camera preview, set this to False
show_camera = True
if (sys.platform == 'linux' and not os.environ.get('DISPLAY')):
    show_camera = False
# Define the regions of interest (ROIs)
roiFront = (60, 60, 340, 5)
roiBack = (100, 112, 240, 5)
rightRoiBack = (240, 112, 120, 5)
leftRoiBack = (100, 112, 180, 5)
roiLeft = (100, 60, 150, 50)
roiRight = (240, 60, 150, 50)

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

def countDistance(frame):

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
        position 
    else:
        position = -128
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
            # Display the image in a window
            cv2.imshow('Image', image)
            cv2.waitKey(1)
            #return image_data
        else:
            print("Response body:", response.text)
    else:
        print("Error:", response.status_code)

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
    countDistance(bin)
    return 0

def help():
    print('python classify-image.py <path_to_model.eim>')

def imageDetection(image):
    modelfile = os.path.join(dir_path, model)
    with ImageImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')
            labels = model_info['model_parameters']['labels']

            img = image
            if img is None:
                print('Failed to load image', args[1])
                exit(1)

            # imread returns images in BGR format, so we need to convert to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            #Prevent image from being cropped by adding a border below it
            img = cv2.copyMakeBorder(img, 0, 160, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

            # get_features_from_image also takes a crop direction arguments in case you don't have square images
            features, cropped = runner.get_features_from_image(img)

            res = runner.classify(features)

            if "classification" in res["result"].keys():
                print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                for label in labels:
                    score = res['result']['classification'][label]
                    print('%s: %.2f\t' % (label, score), end='')
                print('', flush=True)

            elif "bounding_boxes" in res["result"].keys():
                print('Found %d bounding boxes (%d ms.)' % (len(res["result"]["bounding_boxes"]), res['timing']['dsp'] + res['timing']['classification']))
                for bb in res["result"]["bounding_boxes"]:
                    print('\t%s (%.2f): x=%d y=%d w=%d h=%d' % (bb['label'], bb['value'], bb['x'], bb['y'], bb['width'], bb['height']))
                    cropped = cv2.rectangle(cropped, (bb['x'], bb['y']), (bb['x'] + bb['width'], bb['y'] + bb['height']), (255, 0, 0), 1)

            if "visual_anomaly_grid" in res["result"].keys():
                print('Found %d visual anomalies (%d ms.)' % (len(res["result"]["visual_anomaly_grid"]), res['timing']['dsp'] + res['timing']['classification']))
                for grid_cell in res["result"]["visual_anomaly_grid"]:
                    print('\t%s (%.2f): x=%d y=%d w=%d h=%d' % (grid_cell['label'], grid_cell['value'], grid_cell['x'], grid_cell['y'], grid_cell['width'], grid_cell['height']))
                    cropped = cv2.rectangle(cropped, (grid_cell['x'], grid_cell['y']), (grid_cell['x'] + grid_cell['width'], grid_cell['y'] + grid_cell['height']), (255, 125, 0), 1)
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

            center(gray_img)

            # the image will be resized and cropped, save a copy of the picture here
            # so you can see what's being passed into the classifier
            cv2.imwrite('debug.jpg', cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR))

        finally:
            if (runner):
                runner.stop()

def main(argv):
    print('debug')
    try:
        opts, args = getopt.getopt(argv, "h", ["--help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()

    if len(args) != 1:
        help()
        sys.exit(2)
    print('debug')

    model = args[0]

	# Main loop communication
    # Get user input for the command
    
    speed = 100
    turn = 100
    control = speed * 200 + turn
    command = "Integer=" + str(control)
    send_command(command)
    time.sleep(0.2)
    #count = count + 1
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Current time:", current_time)
    # Add a delay if needed

    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #modelfile = os.path.join(dir_path, model)

    print('MODEL: ' + modelfile)
    while True:
        # Send the command
        send_command("VISION")
        time.sleep(0.2)


if __name__ == "__main__":#
   main(sys.argv[1:])