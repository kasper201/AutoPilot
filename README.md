# AutoPilot

## Features

- Detect a face
- Censor faces
- Detect 2 signs

## Installation
OpenMV
- myCam0.1 for face detection requires the censor image to be on the camera

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
34 per class: 82.14 \