import requests
import time

# Nicla server address
server_address = "http://192.168.137.223:8080/"

# Function to send command
def send_command(command):
    response = requests.get(server_address, params={"command": command}, timeout=5)
    print("Sent command:", command)
    print(response)

# Main loop
while True:
    # Get user input for the command
    command = input("Enter command (or 'exit' to quit): ")
    
    # Check if the user wants to exit
    if command.lower() == "exit":
        print("Exiting...")
        break
    
    # Send the command
    send_command(command)
    
    # Add a delay if needed
    time.sleep(1)  # Adjust the delay as needed
