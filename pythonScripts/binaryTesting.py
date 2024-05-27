import cv2

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Binarize the grayscale image to detect black lines
    ret, binary = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY_INV)

    # Display the binary image
    cv2.imshow('Binary Image', binary)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()