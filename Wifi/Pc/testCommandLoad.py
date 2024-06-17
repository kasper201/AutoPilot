import requests
import time
import numpy as np
import cv2

# Nicla server address
server_address = "http://192.168.90.29:8080/"
count = 0

# Create a session object to reuse connections
session = requests.Session()

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
            # Display the image in a window
            cv2.imshow('Image', image)
            cv2.waitKey(1)
            #return image_data
        else:
            print("Response body:", response.text)
    else:
        print("Error:", response.status_code)

# Main loop
while True:
    # Get user input for the command
    # Send the command
    send_command("VISION")
    
    speed = 120
    turn = 110
    control = speed * 200 + turn
    command = "Integer=" + str(control)
    send_command(command)
    time.sleep(0.2)
    count = count + 1
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Current time:", current_time)
    # Add a delay if needed
