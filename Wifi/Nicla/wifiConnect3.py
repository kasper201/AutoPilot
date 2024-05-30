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

def extract_integer_from_string(input_string):
    keyword = "Integer%3D"
    try:
        # Find the start index of the keyword
        start_index = input_string.index(keyword) + len(keyword)
        # Slice the string from the end of the keyword to the end of the string
        substring = input_string[start_index:]
        # Find where the number ends
        end_index = start_index
        while end_index < len(input_string) and input_string[end_index].isdigit():
            end_index += 1
        # Convert the extracted substring to an integer
        integer_value = int(input_string[start_index:end_index])
        return integer_value
    except (ValueError, IndexError) as e:
        return None

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

    response_body = ""
    if command:
        if command == "HELLO":
            print("HELLO has been received")
            response_body = "HELLO response"
        elif command == "STATUS":
            print("STATUS has been received")
            response_body = "STATUS response"
        elif "Integer" in command:
            integer_value = extract_integer_from_string(command)
            if integer_value is not None:
                print(f"Extracted integer: {integer_value}")
                response_body = f"Extracted integer: {integer_value}"
            else:
                print("No integer found in the string.")
                response_body = "No integer found in the string."
        else:
            print("UNKNOWN COMMAND")
            response_body = "UNKNOWN COMMAND"
    else:
        response_body = "INVALID REQUEST"

    # Create the HTTP response
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{response_body}"
    )

    # Send the HTTP response to the client
    client.sendall(http_response.encode('utf-8'))
    client.close()


def start_streaming(s):
    print("Waiting for connections..")
    client, addr = s.accept()
    # set client socket timeout to 5s
    client.settimeout(5.0)
    print("Connected to " + addr[0] + ":" + str(addr[1]))

    # Read request from client
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
    # Should parse client request here

    # Send multipart header
    client.sendall(
        "HTTP/1.1 200 OK\r\n"
        "Server: OpenMV\r\n"
        "Content-Type: multipart/x-mixed-replace;boundary=openmv\r\n"
        "Cache-Control: no-cache\r\n"
        "Pragma: no-cache\r\n\r\n"
    )

    # FPS clock
    clock = time.clock()

    # Start streaming images
    # NOTE: Disable IDE preview to increase streaming FPS.
    while True:
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
        client.settimeout(0.1)
        try:
            data = client.recv(1024)
            if data:
                print("check3")
                handle_client_command(client, data)
        except OSError as e:
            if e.args[0] == 110:  # 110 is 'ETIMEDOUT'
                pass  # Timeout, continue with streaming
            else:
                raise e
        #print(clock.fps())


while True:
    try:
        start_streaming(s)
    except OSError as e:
        print("socket error: ", e)
        # sys.print_exception(e)
