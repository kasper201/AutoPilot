import requests
import time
import numpy as np
import cv2
import os
import sys, getopt
import signal
#from edge_impulse_linux.image import ImageImpulseRunner

# Nicla server address
server_address = "http://192.168.137.173:8080/"
count = 0

# Create a session object to reuse connections
session = requests.Session()


# if you don't want to see a camera preview, set this to False
show_camera = True
if (sys.platform == 'linux' and not os.environ.get('DISPLAY')):
    show_camera = False

# Define roi pixel amounts
twoLinesFront = 60
oneLineBack = 40
twoLinesBack = 10

# Define the regions of interest (ROIs)
roiFront = (60, 20, 380, 5)
roiBack = (100, 95, 240, 5)
rightRoiBack = (240, 95, 120, 5)
leftRoiBack = (100, 95, 180, 5)
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
    calc = round((us_average / 5) * -1)

    if calc > 15:
        calc = 15
    elif calc < -23:
        calc = -23

    #if calc > -4 and calc < 4:
    #    calc = 0
    
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
            #cv2.imwrite('image', cv2.cvtColor(image , cv2.COLOR_RGB2BGR))
            # Display the image in a window
            
            cv2.rectangle(image ,roiLineBack,3 )
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
	img = image
	if img is None:
		print('Failed to load image', args[1])
		exit(1)

	# imread returns images in BGR format, so we need to convert to RGB
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	#Prevent image from being cropped by adding a border below it
	img = cv2.copyMakeBorder(img, 0, 160, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

	
	cropped_img = img[:160, :]
	gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
	_, binary_img = cv2.threshold(gray_img, 101, 255, cv2.THRESH_BINARY_INV)

        #center(gray_img)
	speed = 120
	road_type = detect_road_type(img)
	if (road_type ==  "Unknown"):
		turn = getDirection(binary_img)
	elif (road_type == "Straight line"):
		turn = getDirection(binary_img)
	elif (road_type == "Left turn"):
		turn = getDirection(binary_img)
	elif (road_type == "Right turn"):
		turn = getDirection(binary_img)
	elif (road_type == "t_Intersection"):
		turn = getDirection(binary_img)
	elif (road_type == "Intersection"):
		turn = getDirection(binary_img)
	else:
		speed = 0
		print("WHWUH ERROR NOT A KNOWN ROAD TYPE")
        
	control = speed * 200 + turn
	command = "Integer=" + str(control)
	send_command(command)
	time.sleep(0.2)
	# the image will be resized and cropped, save a copy of the picture here
	# so you can see what's being passed into the classifier
	#cv2.imwrite('debug.jpg', cv2.cvtColor(cropped_w, cv2.COLOR_RGB2BGR))


def detect_road_type(img):
    #img = cv2.imread(image_path)
    
    # Crop the top 160 rows
    cropped_img = img[:160, :]
    
    # Convert to grayscale
    gray_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
    
    # Apply binary threshold to get a binary image (black road becomes white)
    _, binary_img = cv2.threshold(gray_img, 101, 255, cv2.THRESH_BINARY_INV)
    
    # Draw ROIs on the image for visualization
    color_img = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(color_img, (roiFront[0], roiFront[1]), (roiFront[0] + roiFront[2], roiFront[1] + roiFront[3]), (0, 255, 0), 2)
    cv2.rectangle(color_img, (roiBack[0], roiBack[1]), (roiBack[0] + roiBack[2], roiBack[1] + roiBack[3]), (0, 0, 255), 2)
    cv2.rectangle(color_img, (rightRoiBack[0], rightRoiBack[1]), (rightRoiBack[0] + rightRoiBack[2], rightRoiBack[1] + rightRoiBack[3]), (255, 0, 0), 2)
    cv2.rectangle(color_img, (leftRoiBack[0], leftRoiBack[1]), (leftRoiBack[0] + leftRoiBack[2], leftRoiBack[1] + leftRoiBack[3]), (255, 255, 0), 2)
    cv2.rectangle(color_img, (roiBack2[0], roiBack2[1]), (roiBack2[0] + roiBack2[2], roiBack2[1] + roiBack2[3]), (255, 255, 255), 2)
    
    # Determine road type based on ROIs
    road_type = "Unknown"
    if straightLine(binary_img):
        road_type = "Straight line"
    elif leftTurn(binary_img):
        road_type = "Left turn"
    elif rightTurn(binary_img):
        road_type = "Right turn"
    elif t_intersection(binary_img):
        road_type = "t_Intersection"
    elif intersection(binary_img):
        road_type = "Intersection"
       # Display the road type on the image
    cv2.putText(color_img, road_type, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Road detection", color_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return road_type


def main(argv):
    print('debug')
    

    #model = args[0]

	# Main loop communication
    # Get user input for the command

    #count = count + 1
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Current time:", current_time)
    # Add a delay if needed

    #dir_path = os.path.dirname(os.path.realpath(__file__))
    #modelfile = os.path.join(dir_path, model)

   
    while True:
        # Send the command
        send_command("VISION")
        time.sleep(0.2)


if __name__ == "__main__":#
	main(sys.argv[1:])
