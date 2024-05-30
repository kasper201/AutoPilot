import requests
import time

# Nicla server address
server_address = "http://192.168.137.115:8080/"
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
            # You can further process or save the image data here
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
    
    command = "Integer=" + str(count)
    send_command(command)
    count = count + 1
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print("Current time:", current_time)
    # Add a delay if needed
