# AutoPilot

- [AutoPilot](#autopilot)
- [Nicla side](#nicla-side)
  - [Way 1](#way-1)
  - [Way 2](#way-2)
- [PC side](#pc-side)
  - [Setup](#setup)
  - [Camera on virtual machine](#camera-on-virtual-machine)
  - [Running sample](#running-sample)
  - [Running sample with camera in arg](#running-sample-with-camera-in-arg)
  - [No Xv port](#no-xv-port)
  - [Pipeline doesnt want to pause](#pipeline-doesnt-want-to-pause)
  - [Not-negotiated](#not-negotiated)
  - [GST sanity check](#gst-sanity-check)

# Nicla side
## Way 1
- Build for Nicla Vision
- Run script
- edge-impulse-run-impulse --debug

Double tap reset to be able to flash again

## Way 2
- Build for Arduino Nicla Vision
- Run script 
- Result is visible on framebuffer

# PC side
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
## Running sample
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

## GST sanity check
gst-launch-1.0 videotestsrc ! autovideosink

[//]: # (For any further comments)
