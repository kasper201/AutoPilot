import cv2
import numpy as np
def process_frame(frame):
    # Define the region of interest (ROI) as the top 185 pixels of the frame
    roi = frame[:185, :]
    
    # Convert the ROI to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
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
    
    # Draw the left lane lines
    for line in left_lane_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(roi, (x1, y1), (x2, y2), (0, 255, 0), 3)
    
    # Draw the right lane lines
    for line in right_lane_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(roi, (x1, y1), (x2, y2), (0, 255, 0), 3)
    
    # Determine the car position relative to the lanes
    if len(left_lane_lines) > 0 and len(right_lane_lines) > 0:
        # Calculate the midpoint of the lanes
        left_x = int(np.mean([line[0][0] for line in left_lane_lines]))
        right_x = int(np.mean([line[0][2] for line in right_lane_lines]))
        road_center = (left_x + right_x) // 2
        frame_center = roi.shape[1] // 2
        
        # Draw the road center line
        cv2.line(roi, (road_center, 0), (road_center, 185), (255, 0, 0), 2)
        
        # Draw the frame center line
        cv2.line(roi, (frame_center, 0), (frame_center, 185), (0, 0, 255), 2)
        
        # Determine the position of the car relative to the road
        if road_center < frame_center - 20:
            position = "Steer left"
        elif road_center > frame_center + 20:
            position = "Steer right"
        else:
            position = "On Track"
    else:
        position = "Road Not Detected"
    
    # Display the results on the frame
    cv2.putText(frame, position, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Replace the ROI back into the frame
    frame[:185, :] = roi
    
    return frame

def main():
    # Load the image from file
    image_path = '00011.jpg'
    frame = cv2.imread(image_path)
    
    if frame is None:
        print(f"Error: Unable to load image at {image_path}")
        return
    
    # Process the frame to detect the road and car position
    processed_frame = process_frame(frame)
    
    # Display the resulting frame
    cv2.imshow('Road Detection', processed_frame)
    
    # Wait indefinitely until a key is pressed
    cv2.waitKey(0)
    
    # Destroy all windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


    # [flits@KaspersPC pythonScripts]$ source //home/flits/SchoolProjects/AutoPilot/myenv/bin/activate
 # (myenv) [flits@KaspersPC pythonScripts]$ 


