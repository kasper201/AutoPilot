import sensor
import time
import network
import socket

SSID = "Nicla"  # Network SSID
KEY = "Weerstation"  # Network key
HOST = ""  # Use first available interface
PORT = 8080  # Arbitrary non-privileged port

# Init sensor
sensor.reset()
sensor.set_framesize(sensor.HVGA)
sensor.set_pixformat(sensor.RGB565)
sensor.set_vflip(True)
sensor.ioctl(sensor.IOCTL_SET_FOV_WIDE, True)

# Init wlan module and connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, KEY)

while not wlan.isconnected():
    print('Trying to connect to "{:s}"...'.format(SSID))
    time.sleep_ms(1000)

# We should have a valid IP now via DHCP
print("WiFi Connected ", wlan.ifconfig())

# Create server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

# Bind and listen
s.bind([HOST, PORT])
s.listen(5)

# Set server socket to blocking
s.setblocking(True)

# Function to handle commands from client
def handle_client_command(client, data):
    """Handles commands sent from the client."""
    command = None
    try:
        # Parse HTTP request to extract command parameter
        request_lines = data.decode('utf-8').split('\r\n')
        first_line = request_lines[0]
        # Split the first line by spaces to isolate the command part
        command_parts = first_line.split()
        # Check if the first line contains the command
        if len(command_parts) > 1 and command_parts[0] == "GET":
            # Extract the command from the URL
            url = command_parts[1]
            command_index = url.find("command=")
            if command_index != -1:
                command = url[command_index + len("command="):]
    except Exception as e:
        print("Error parsing request:", e)

    print(command)
    if command:
        if command == "HELLO":
            print("check")
            client.sendall(b"HELLO FROM OPENMV\r\n")
        elif command == "STATUS":
            client.sendall(b"STATUS: OK\r\n")
        else:
            client.sendall(b"UNKNOWN COMMAND\r\n")
    else:
        client.sendall(b"INVALID REQUEST\r\n")


# FPS clock
clock = time.clock()

# Start streaming function
def start_streaming(client):
    while True:
        try:
            # Stream image
            clock.tick()  # Track elapsed milliseconds between snapshots().
            frame = sensor.snapshot()
            cframe = frame.compressed(quality=35)
            header = (
                "\r\n--openmv\r\n"
                "Content-Type: image/jpeg\r\n"
                "Content-Length:" + str(cframe.size()) + "\r\n\r\n"
            )
            client.sendall(header)
            client.sendall(cframe)
            print(clock.fps())

            # Attempt to receive command with timeout
            client.settimeout(0.1)
            try:
                data = client.recv(1024)
                if data:
                    print("check2")
                    handle_client_command(client, data)
            except OSError as e:
                if e.args[0] == 110:  # 110 is 'ETIMEDOUT'
                    pass  # Timeout, continue with streaming
                else:
                    raise e

        except OSError as e:
            print("socket error: ", e)
            break

# Main loop
while True:
    print("Waiting for connections..")
    client, addr = s.accept()
    # set client socket timeout to 5s
    client.settimeout(5.0)
    print("Connected to " + addr[0] + ":" + str(addr[1]))

    # Send multipart header for image streaming
    client.sendall(
        "HTTP/1.1 200 OK\r\n"
        "Server: OpenMV\r\n"
        "Content-Type: multipart/x-mixed-replace;boundary=openmv\r\n"
        "Cache-Control: no-cache\r\n"
        "Pragma: no-cache\r\n\r\n"
    )

    # Start streaming
    start_streaming(client)

    # Close client socket after streaming ends
    client.close()
