import requests
import time
import numpy as np
import cv2
import os
import sys, getopt
import signal
from edge_impulse_linux.image import ImageImpulseRunner

# Nicla server address
server_address = "http://192.168.93.29:8080/"
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

# Define roi pixel amounts
twoLinesFront = 103
oneLineBack = 106
twoLinesBack = 10

# Define the regions of interest (ROIs)
roiFront = (60, 60, 340, 5)
roiBack = (100, 112, 240, 5)
rightRoiBack = (240, 112, 120, 5)
leftRoiBack = (100, 112, 180, 5)
roiLeft = (100, 60, 150, 50)
roiRight = (240, 60, 150, 50)

roiBack2 = (100, 125, 240, 5)

roiLineBack = (0, 60, 480, 5)
roiLineFront = (0, 15, 480, 5)

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
def count_white_pixels(img, roi, pattern_name, pixels):
    roi_img = img[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    mean_value = cv2.mean(roi_img)[0]
    # For manual figuring out the value
    print(f"{pattern_name} mean ROI {roi}: {mean_value}")
    # Threshold for enough white pixels from line
    return mean_value >= pixels


def getDirection(img):
    right1 = find_first_white_pixel_right(img, roiLineFront)
    right2 = find_first_white_pixel_right(img, roiLineBack)
    left1 = find_first_white_pixel_left(img, roiLineFront)
    left2 = find_first_white_pixel_left(img, roiLineBack)
    average1 = round((left1 + right1) / 2)
    average2 = round((left2 + right2) / 2) + 19
    print(f"average2: {average2}" )

    us_average = average2 - 240
    calc = round((us_average / 3) * -1)

    if calc > 20:
        calc = 20
    elif calc < -20:
        calc = -20

    if calc > -4 and calc < 4:
        calc = 0
    
    return  calc + 100







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
    return count_white_pixels(img, roiFront, "Straight line", twoLinesFront) and count_white_pixels(img, roiBack, "Straight line", twoLinesFront)

def intersection(img):
    a = count_white_pixels(img, roiFront, "Intersection", twoLinesFront) and not count_white_pixels(img, roiBack, "Intersection", twoLinesBack)
    return a and count_white_pixels(img, roiBack2, "Intersection", twoLinesBack)

def t_intersection(img):
    return count_white_pixels(img, roiFront, "t_Intersection", twoLinesFront) and not count_white_pixels(img, roiBack, "t_Intersection", twoLinesBack)

def leftTurn(img):
    return count_white_pixels(img, roiFront, "Left turn", twoLinesFront) and count_white_pixels(img, leftRoiBack, "Left turn", oneLineBack)

def rightTurn(img):
    return count_white_pixels(img, roiFront, "Right turn", twoLinesFront) and count_white_pixels(img, rightRoiBack, "Right turn", oneLineBack)

def turnRight():
    speed = 50
    turn = 99
    control = speed * 200 + turn
    command = "Integer=" + str(control)
    send_command(command)
    
def turnLeft():
    speed = 50
    turn = -99
    control = speed * 200 + turn
    command = "Integer=" + str(control)
    send_command(command)

def help():
    print('python classify-image.py <path_to_model.eim>')

def signNumbers(labels):
    return {'50':"SIGN Integer=4",
            'B01':"SIGN Integer=5",
            'b02':"",
            'b07':"SIGN Integer=6",
            'c02':"",
            'c04':"SIGN Integer=7",
            'e01':"",
            'e02':"",
            'F01':"",
            'green':"SIGN Integer=3",
            'l08':"",
            'orange':"SIGN Integer=2",
            'red':"SIGN Integer=1",
    }[labels]

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
            #if len(res["result"]["bounding_boxes"]) >= 1:
            #   print('Sign found!'
            if len(res["result"]["bounding_boxes"]) >= 1:
                print('Sign found!')

            if "classification" in res["result"].keys():
                print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                for label in labels:
                    score = res['result']['classification'][label]
                    print('%s: %.2f\t' % (label, score), end='')
                print('', flush=True)

            elif "bounding_boxes" in res["result"].keys():
                print('Found %d bounding boxes (%d ms.)' % (len(res["result"]["bounding_boxes"]), res['timing']['dsp'] + res['timing']['classification']))
                for bb in res["result"]["bounding_boxes"]:
                    # Send string of label
                    send_command(signNumbers(bb['label']))
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

            #center(gray_img)
            speed = 120
            turn = getDirection(binary_img)
            control = speed * 200 + turn
            command = "Integer=" + str(control)
            send_command(command)
            time.sleep(0.2)

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