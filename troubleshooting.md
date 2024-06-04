# AutoPilot

- [AutoPilot](#autopilot)
- [Model on Nicla side](#model-on-nicla-side)
  - [Way 1](#way-1)
  - [Way 2](#way-2)
- [Model on PC side](#model-on-pc-side)
  - [Setup](#setup)
  - [Camera on virtual machine](#camera-on-virtual-machine)
  - [General GStreamer error](#general-gstreamer-error)
  - [Running sample with camera in arg](#running-sample-with-camera-in-arg)
  - [No Xv port](#no-xv-port)
  - [Pipeline doesnt want to pause](#pipeline-doesnt-want-to-pause)
  - [Not-negotiated](#not-negotiated)
  - [Pipeline have not been created](#pipeline-have-not-been-created)
  - [Ignorable errors](#ignorable-errors)
  - [GST sanity check](#gst-sanity-check)
- [Wi-fi](#wi-fi)
  - [Setup hotspot xubuntu vm](#setup-hotspot-xubuntu-vm)
  - [No MAC adress](#no-mac-adress)
  - [Connection lost](#connection-lost)
- [Hotspot Windows, terminal Linux](#hotspot-windows-terminal-linux)
  - [Hotspot Windows](#hotspot-windows)
  - [Pipe connection to Linux](#pipe-connection-to-linux)
  - [Waiting for guest process (flags 0x1) failed: Error VERR\_ACCESS\_DENIED for guest process](#waiting-for-guest-process-flags-0x1-failed-error-verr_access_denied-for-guest-process)
  - [Scancode saending](#scancode-saending)
  - [ConnectionResetError(10054)](#connectionreseterror10054)
  - [Refresh image](#refresh-image)
  - [Hotspot other device, virtual machine Linux](#hotspot-other-device-virtual-machine-linux)

# Model on Nicla side
## Way 1
- Build for Nicla Vision
- Run script
- edge-impulse-run-impulse --debug

Double tap reset to be able to flash again

## Way 2
- Build for Arduino Nicla Vision
- Run script 
- Result is visible on framebuffer

# Model on PC side
## Setup
- Haven't been able to get this running on Windows, so all steps from now on are done on Linux

```
pip3 install edge_impulse_linux

sudo apt install -y curl
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
sudo apt install -y gcc g++ make build-essential nodejs sox gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps
npm config set user root && sudo npm install edge-impulse-linux -g --unsafe-perm

edge-impulse-linux
```

Building model:
```
edge-impulse-linux-runner --download modelfile.eim
```

Running model:
```
python3 classify.py modelfile.eim 0
python3 classify-image.py modelfile.eim 00010.jpg
```
## Camera on virtual machine
- Install Oracle VM VirtualBox Extension Pack 
- Get a list of cameras on host with:
VBoxManage list webcams
- Attach camera:
VboxManage controlvm "[VM name]" webcam attach [.Camera number]

for example: >VboxManage controlvm "Linux95" webcam attach .1
- Check if camera shows up on vm side: ls /dev/video*
- Check if camera works: ffplay /dev/video0
- 
## General GStreamer error
```
C:\home\npc\Documents\edge> python3 classify.py modelfile.eim
MODEL: /home/npc/Documents/edge/modelfile.eim
Loaded runner for "nope / objectFOMO"
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src0 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (888) open OpenCV | GStreamer warning: unable to start pipeline
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (480) isPipelinePlaying OpenCV | GStreamer warning: GStreamer: pipeline have not been created
Camera V4L2 (480.0 x 640.0) in port 0 selected.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.

(python3:38634): GStreamer-CRITICAL **: 12:09:05.580: gst_caps_get_structure: assertion 'GST_IS_CAPS (caps)' failed

(python3:38634): GStreamer-CRITICAL **: 12:09:05.580: gst_structure_get_int: assertion 'structure != NULL' failed
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (914) open OpenCV | GStreamer warning: cannot query video width/height

(python3:38634): GStreamer-CRITICAL **: 12:09:05.580: gst_structure_get_fraction: assertion 'structure != NULL' failed
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (920) open OpenCV | GStreamer warning: cannot query video fps
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (935) open OpenCV | GStreamer warning: Cannot query video position: status=0, value=-1, duration=-1
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (515) startPipeline OpenCV | GStreamer warning: unable to start pipeline
^CInterrupted
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (480) isPipelinePlaying OpenCV | GStreamer warning: GStreamer: pipeline have not been created

```
## Running sample with camera in arg
```
python3 classify.py modelfile.eim 0
MODEL: /home/npc/Documents/edge/modelfile.eim
Loaded runner for "nope / objectFOMO"
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src0 reported: Internal data stream error.

(python3:1530): GStreamer-CRITICAL **: 20:21:17.012: gst_caps_get_structure: assertion 'GST_IS_CAPS (caps)' failed

(python3:1530): GStreamer-CRITICAL **: 20:21:17.012: gst_structure_get_int: assertion 'structure != NULL' failed
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (914) open OpenCV | GStreamer warning: cannot query video width/height

(python3:1530): GStreamer-CRITICAL **: 20:21:17.012: gst_structure_get_fraction: assertion 'structure != NULL' failed
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (920) open OpenCV | GStreamer warning: cannot query video fps
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (935) open OpenCV | GStreamer warning: Cannot query video position: status=0, value=-1, duration=-1
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src0 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (515) startPipeline OpenCV | GStreamer warning: unable to start pipeline
Traceback (most recent call last):
  File "classify.py", line 129, in <module>
    main(sys.argv[1:])
  File "classify.py", line 95, in main
    raise Exception("Couldn't initialize selected camera.")
Exception: Couldn't initialize selected camera.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (480) isPipelinePlaying OpenCV | GStreamer warning: GStreamer: pipeline have not been created
```

Fix: Not sure how, it worked after too many attempts
## No Xv port
gst-launch-1.0 v4l2src ! xvimagesink

```
C:\home\npc\Documents\edge> gst-launch-1.0 v4l2src ! xvimagesink
Setting pipeline to PAUSED ...
ERROR: Pipeline doesn't want to pause.
ERROR: from element /GstPipeline:pipeline0/GstXvImageSink:xvimagesink0: Could not initialise Xv output
Additional debug info:
xvimagesink.c(1773): gst_xv_image_sink_open (): /GstPipeline:pipeline0/GstXvImageSink:xvimagesink0:
No Xv Port available
Setting pipeline to NULL ...
Freeing pipeline ...
```
Tried:
sudo apt install libxv-dev

sudo gst-launch-1.0 v4l2src ! xvimagesink

```sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio```

Turn on the camera doesnt work here

## Pipeline doesnt want to pause
gst-launch-1.0 videotestsrc ! xvimagesink

gst-launch-1.0 v4l2src ! autovideosink

```
C:\home\npc\Documents\edge> gst-launch-1.0 v4l2src ! autovideosink
Setting pipeline to PAUSED ...
ERROR: Pipeline doesn't want to pause.
Got context from element 'autovideosink0': gst.gl.GLDisplay=context, gst.gl.GLDisplay=(GstGLDisplay)"\(GstGLDisplayX11\)\ gldisplayx11-0";
ERROR: from element /GstPipeline:pipeline0/GstV4l2Src:v4l2src0: Cannot identify device '/dev/video0'.
Additional debug info:
v4l2_calls.c(607): gst_v4l2_open (): /GstPipeline:pipeline0/GstV4l2Src:v4l2src0:
system error: No such file or directory
Setting pipeline to NULL ...
Freeing pipeline ...
C:\home\npc\Documen
```

Turn on the camera, and make sure it's recognized.

## Not-negotiated
```
C:\home\npc\Documents\edge> gst-launch-1.0 v4l2src ! autovideosink
Setting pipeline to PAUSED ...
Pipeline is live and does not need PREROLL ...
Got context from element 'autovideosink0': gst.gl.GLDisplay=context, gst.gl.GLDisplay=(GstGLDisplay)"\(GstGLDisplayX11\)\ gldisplayx11-0";
Setting pipeline to PLAYING ...
New clock: GstSystemClock
ERROR: from element /GstPipeline:pipeline0/GstV4l2Src:v4l2src0: Internal data stream error.
Additional debug info:
gstbasesrc.c(3072): gst_base_src_loop (): /GstPipeline:pipeline0/GstV4l2Src:v4l2src0:
streaming stopped, reason not-negotiated (-4)
Execution ended after 0:00:00.001278130
Setting pipeline to NULL ...
Freeing pipeline ...
```

Not fixed 

## Pipeline have not been created
```
Loaded runner for "nope / objectFOMO"
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src0 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (888) open OpenCV | GStreamer warning: unable to start pipeline
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (480) isPipelinePlaying OpenCV | GStreamer warning: GStreamer: pipeline have not been created
Camera V4L2 (480.0 x 640.0) in port 0 selected.
```
Restart vm
## Ignorable errors
```
C:\home\npc\Documents\edge> python3 classify.py modelfile.eim 0
MODEL: /home/npc/Documents/edge/modelfile.eim
Loaded runner for "nope / objectFOMO"
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src0 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (888) open OpenCV | GStreamer warning: unable to start pipeline
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (480) isPipelinePlaying OpenCV | GStreamer warning: GStreamer: pipeline have not been created
Camera V4L2 (480.0 x 640.0) in port 0 selected.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (1758) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module v4l2src1 reported: Internal data stream error.
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (888) open OpenCV | GStreamer warning: unable to start pipeline
[ WARN:0] global ../modules/videoio/src/cap_gstreamer.cpp (480) isPipelinePlaying OpenCV | GStreamer warning: GStreamer: pipeline have not been created
Found 0 bounding boxes (5 ms.)
Found 1 bounding boxes (0 ms.)
	B01 (0.63): x=16 y=48 w=8 h=8
Found 1 bounding boxes (0 ms.)
```
## GST sanity check
gst-launch-1.0 videotestsrc ! autovideosink

# Wi-fi
## Setup hotspot xubuntu vm
```
1. Under Editing Wi-Fi dialog, fill in the options as the following:
    Connection name: Wi-Fi Connection 1
    SSID: master-hotspot
    Mode: Hotspot
    Wi-Fi Security: WPA Personal
    Password: <your_password>
    Save
2. Click wifi icon > Create a new wi-fi network > fill in the options:
    Connection: Wi-Fi Connection 1 (or the same as the above)
    Create
3. Connection Established message will show with "master-hotspot" as the connected network. Other computer, laptop and phone around will see your hotspot under this name.
4. Connect other device to your newly created hotspot. 
Done.
```
This approach doesn't work on the virtual machine itself.
## No MAC adress
```
C:\home\npc> ifconfig | grep HWaddr

Command 'ifconfig' not found, but can be installed with:

sudo apt install net-tools
```

## Connection lost
```
debug
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 159, in _new_conn
    conn = connection.create_connection(
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 84, in create_connection
    raise err
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 74, in create_connection
    sock.connect(sa)
TimeoutError: [Errno 110] Connection timed out

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 666, in urlopen
    httplib_response = self._make_request(
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 388, in _make_request
    conn.request(method, url, **httplib_request_kw)
  File "/usr/lib/python3.8/http/client.py", line 1256, in request
    self._send_request(method, url, body, headers, encode_chunked)
  File "/usr/lib/python3.8/http/client.py", line 1302, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.8/http/client.py", line 1251, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
  File "/usr/lib/python3.8/http/client.py", line 1011, in _send_output
    self.send(msg)
  File "/usr/lib/python3.8/http/client.py", line 951, in send
    self.connect()
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 187, in connect
    conn = self._new_conn()
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 171, in _new_conn
    raise NewConnectionError(
urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPConnection object at 0x7f72e278e6d0>: Failed to establish a new connection: [Errno 110] Connection timed out

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/requests/adapters.py", line 439, in send
    resp = conn.urlopen(
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 720, in urlopen
    retries = retries.increment(
  File "/usr/lib/python3/dist-packages/urllib3/util/retry.py", line 436, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='192.168.90.29', port=8080): Max retries exceeded with url: /?command=VISION (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f72e278e6d0>: Failed to establish a new connection: [Errno 110] Connection timed out'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "test.py", line 255, in <module>
    main(sys.argv[1:])
  File "test.py", line 235, in main
    send_command("VISION")
  File "test.py", line 96, in send_command
    response = session.get(server_address, params={"command": command})
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 548, in get
    return self.request('GET', url, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 535, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 648, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPConnectionPool(host='192.168.90.29', port=8080): Max retries exceeded with url: /?command=VISION (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f72e278e6d0>: Failed to establish a new connection: [Errno 110] Connection timed out'))

```
# Hotspot Windows, terminal Linux
## Hotspot Windows
- Select Start , then select Settings  > Network & Internet > Mobile hotspot.
For Share my Internet connection from, choose the Internet connection you want to share.
- If desired, select Edit > enter a new network name(Nicla) and password(Weerstation) > Save.
Turn on Share my Internet connection with other devices.

## Pipe connection to Linux
Pipe way doesn't execute the python script.

## Waiting for guest process (flags 0x1) failed: Error VERR_ACCESS_DENIED for guest process
```
VBoxManage guestcontrol “Linux95” run --exe /home/npc/Documents/autoPilot/edge/classify-image.py --username [username] --password [pw] --wait-stdout --wait-stderr
```
```
VBoxManage.exe: error: Waiting for guest process (flags 0x1) failed: Error VERR_ACCESS_DENIED for guest process "/home/npc/Documents/autoPilot/edge/classify-image.py" occurred

VBoxManage.exe: error: Details: code VBOX_E_IPRT_ERROR (0x80bb0005), component GuestProcessWrap, interface IGuestProcess, callee IUnknown
VBoxManage.exe: error: Context: "WaitForArray(ComSafeArrayAsInParam(aWaitStartFlags), gctlRunGetRemainingTime(msStart, cMsTimeout), &waitResult)" at line 1397 of file VBoxManageGuestCtrl.cpp

```
## Scancode saending
```
VBoxManage controlvm Linux95 keyboardputscancode 1d 38 e0  14
```

```
VBoxManage guestcontrol [VMname] --username [username] --password [password] run --exe "/usr/bin/python3" -- [python script path] [model path] [image path]
```

## ConnectionResetError(10054)
```
C:\Users\NPC\Documents\sharedVM>python testCommandLoad.py
Traceback (most recent call last):
  File "C:\Python311\Lib\site-packages\urllib3\connectionpool.py", line 790, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\urllib3\connectionpool.py", line 536, in _make_request
    response = conn.getresponse()
               ^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\urllib3\connection.py", line 461, in getresponse
    httplib_response = super().getresponse()
                       ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\http\client.py", line 1378, in getresponse
    response.begin()
  File "C:\Python311\Lib\http\client.py", line 318, in begin
    version, status, reason = self._read_status()
                              ^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\http\client.py", line 279, in _read_status
    line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\socket.py", line 706, in readinto
    return self._sock.recv_into(b)
           ^^^^^^^^^^^^^^^^^^^^^^^
ConnectionResetError: [WinError 10054] An existing connection was forcibly closed by the remote host

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Python311\Lib\site-packages\requests\adapters.py", line 486, in send
    resp = conn.urlopen(
           ^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\urllib3\connectionpool.py", line 844, in urlopen
    retries = retries.increment(
              ^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\urllib3\util\retry.py", line 470, in increment
    raise reraise(type(error), error, _stacktrace)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\urllib3\util\util.py", line 38, in reraise
    raise value.with_traceback(tb)
  File "C:\Python311\Lib\site-packages\urllib3\connectionpool.py", line 790, in urlopen
    response = self._make_request(
               ^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\urllib3\connectionpool.py", line 536, in _make_request
    response = conn.getresponse()
               ^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\urllib3\connection.py", line 461, in getresponse
    httplib_response = super().getresponse()
                       ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\http\client.py", line 1378, in getresponse
    response.begin()
  File "C:\Python311\Lib\http\client.py", line 318, in begin
    version, status, reason = self._read_status()
                              ^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\http\client.py", line 279, in _read_status
    line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\socket.py", line 706, in readinto
    return self._sock.recv_into(b)
           ^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.ProtocolError: ('Connection aborted.', ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\NPC\Documents\sharedVM\testCommandLoad.py", line 58, in <module>
    send_command("VISION")
  File "C:\Users\NPC\Documents\sharedVM\testCommandLoad.py", line 19, in send_command
    response = session.get(server_address, params={"command": command})
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\requests\sessions.py", line 602, in get
    return self.request("GET", url, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\requests\sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\requests\sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python311\Lib\site-packages\requests\adapters.py", line 501, in send
    raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None))

```

## Refresh image
Virtual machine needs to have the image folder manually refreshed, or the images wont get loaded on time for the script.

## Hotspot other device, virtual machine Linux
- Connect to hotspot
- Check the IP on Nicla's side and adjust it in the code on Linux side if needed
- run the script

[//]: # (For any further comments)
