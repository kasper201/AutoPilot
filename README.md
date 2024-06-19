# AutoPilot

- [Features](#features)
- [Setup](#setup)
    - [Necessary items](#necessary-items)
    - [Expected to already be installed](#expected-to-already-be-installed)
    - [Router](#router)
    - [Nicla Vision](#nicla-vision)
    - [Zumo](#zumo)
    - [Computer](#computer)
        - [Debian based](#debian-based)
        - [Arch based](#arch-based)

## Features

- Detects 10+ signs
- Follows a road

## Setup
To get the robot to follow the road with sign detection a few programs must be installed. To have it function one should use Linux. This setup guid shows how to install for Debian based OS's and Arch based OS's.

### Necessary items
 - Computer
 - Arduino Nicla Vision
 - Pololu Zumo 32U4
 - Nicla Vision to Zumo printplate
 - Router

### Expected to already be installed
 - Python
 - npm
 - openMV
 - Arduino IDE or similar

### Router
Since the Nicla and the computer communicate via WiFi a kind of router is necessary. The router can be anything. A hotspot on a mobile phone or laptop is already good enough as long as the router doesn't introduce a significant delay. 

Make sure the routers WiFi name is ``Nicla`` and the password should be ``Weerstation``.

### Nicla Vision
On the nicla flash the code from Integration/WiFiToZumo.py using the openMV application on the Nicla Vision. The code **will get lost** on power loss so make sure either the Zumo or the Nicla has power.

### Zumo
In the IDE make sure you have installed the ``32U4`` library and its dependencies. Then connect to the Zumo and flash it. The board is an ``Arduino Leonardo`` board.

### Computer
first install openCV for python
```
pip3 install openCV-python
```

If for either Debian based or Arch based there is the error:
```
error: externally-managed-environment
```
Anywhere in the process. Make sure you put ``--break-system-packages`` at the end of the pip3 command.

#### Debian based
```
pip3 install edge_impulse_linux

sudo apt install -y curl
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
sudo apt install -y gcc g++ make build-essential nodejs sox gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps
npm config set user root && sudo npm install edge-impulse-linux -g --unsafe-perm

edge-impulse-linux
```
Access to the edge impulse is only necessary if you want to download the model from edge impulse. The model is also available on the github.

Building model(optional):
```
edge-impulse-linux-runner --download modelfile.eim
``` 
Building the model file is only necessary if not using the one supplied on github.

running model
```
python3 openCV.py
```
To run the program use ``openCV.py`` in the folder ``opencv``. Make sure that the model is in the **same** folder and named ``modelfileV3.eim``.

#### Arch based
```
pip3 install edge_impulse_linux

Paru -S curl
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
npm install edge-impulse-linux -g --unsafe-perm

edge-impulse-linux
```
Access to the edge impulse is only necessary if you want to download the model from edge impulse. The model is also available on the github.

Building model(optional):
```
edge-impulse-linux-runner --download modelfile.eim
``` 
Building the model file is only necessary if not using the one supplied on github.

running model
```
python3 openCV.py
```
To run the program use ``openCV.py`` in the folder ``opencv``. Make sure that the model is in the **same** folder and named ``modelfileV3.eim``.

<!--
OpenMV
- myCam0.1 for face detection requires the censor image to be on the camera


## Coloured line finder
- Run findColouredLine on the Nicla
- Adjust h value if needed
- 
## FOMO model
- Put the files from modelData in the Nicla.
- Run FOMOmodelV1 on the Nicla.
- Currently it recognizes 2 signs well, 1 was recognized during testing but not actual usage and the last sign is not recognized at all.

## Images needed for accuracy:
8 per class: 0% accuracy\
12 per class: 30% accuracy\
19 per class: 40% accuracy \
25 per class: 88.89% accuracy\ 
27 per class: 80.95% accuracy \
30 per class: 62.50% accuracy \
---resplitting training data:\
30 per class: 66.67% accuracy \
34 per class: 60% accuracy \
--adjusted training data:\
34 per class: 82.14 \-->