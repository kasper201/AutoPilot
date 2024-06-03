import cv2
import numpy as np

# Read the image
image = cv2.imread('selfie.jpg')

# Define a kernel (e.g., a simple 3x3 box blur kernel)
kernel = [[1,0,0], [ 1,1,0], [1,1,0]]#np.ones((3, 3), np.float32) / 9

# Apply the kernel to the image using filter2D
filtered_image = cv2.filter2D(image, -1, kernel)

# Display the original and filtered images
cv2.imshow('Original Image', image)
cv2.imshow('Filtered Image', filtered_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
