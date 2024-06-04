import cv2
import numpy as np

# Define roi pixel amounts
twoLinesFront = 50
oneLineBack = 30
twoLinesBack = 10

# Define the regions of interest (ROIs) in the format (x, y, width, height)
# Define the regions of interest (ROIs)
roiFront = (60, 60, 340, 5)
roiBack = (100, 110, 240, 5)
rightRoiBack = (240, 110, 120, 5)
leftRoiBack = (100, 110, 180, 5)

roiBack2 = (100, 125, 240, 5)

def count_white_pixels(img, roi, pattern_name, pixels):
    x, y, w, h = roi
    roi_img = img[y:y+h, x:x+w]
    mean_value = cv2.mean(roi_img)[0]
    # Debugging print statement
    print(f"{pattern_name} mean ROI {roi}: {mean_value}")
    return mean_value >= pixels

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

def detect_road_type(image_path):
    img = cv2.imread(image_path)
    
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
    #elif t_intersection(binary_img):
    #    road_type = "t_Intersection"
    elif intersection(binary_img):
        road_type = "Intersection"
    
    # Display the road type on the image
    cv2.putText(color_img, road_type, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Road detection", color_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_road_type("00013.jpg")