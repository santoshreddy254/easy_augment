
# Realsense Augmentor

[![Build Status](https://travis-ci.org/santoshreddy254/realsense_augmentor.svg?branch=master)](https://travis-ci.org/santoshreddy254/realsense_augmentor)

> End to end software to capture new objects using RGBD camera and augment them to get a annotated dataset to train deep nets

1) Pipeline to artificial generate annotated data for training deep learning models.
2) Pipeline includes starting from capturing images using provided camera (Realsense),
generate semantic labels of the captured image and then generate the artificial images.
3) GUI required for the end user from capturing to labelling and generating new data.

![](header.png)
## Requirements
1) Ubuntu 16.04 (Testing for Ubuntu 18.04)
2) Intel Realsense Camera
3) Processer intel i5 or higher
5) python 3.5

## Limitations
1) Number of classes captured should be more than or equal to 2.
2) Only one object in the scene to segment, not supported for multiple objects.

## Installation
### Build from source
Linux:

```sh
git clone https://github.com/santoshreddy254/realsense_augmentor.git
cd realsense_augmentor
./setup.sh
```
### From pip
```
pip3 install easy-augment
```

## Usage example

```sh
cd realsense_augmentor
python3 src/main.py
```
1) Start page will be as below and select the path to save the captured images.
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/main_window.png)
2) On selecting capture next window will look like
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/capture_window.png)
3) On selectin Have Annotations
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/annotate_window.png)
Steps after selecting capture option and selecting save path
4) Next window will have image and mask of corresponding object. Capture as many as images per classe.
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/window_02-1.png)
5) Click add to add new class label.
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/window_02-2.png)
6) Click save to save the current displyed image and semantic label.
7) Click finish once done with capturing all the images.
8) Folder name \textbf{captured_data} in selected save path will have images, labels and labels.txt
9) Input parameters to generate artificial images need to be filled next window.
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/window_03.png)
10) Click OK once setting up the parameters.
11) Folder name \textbf{augmented} in selected save path will have artificial images.

Steps after selecting Have annotations
12) Select the location of images and corresponding annotations
13) Select save path
14) Select labels.txt file path
15) Follow the steps from Step 9

## Release History


* 1.0.0
    * First release for crowd testing

## Contributors
* Santosh Muthireddy              – https://github.com/santoshreddy254
* Naresh Kumar Gurulingan         - https://github.com/NareshGuru77
* Deepan Chakravarthi Padmanabhan - https://github.com/DeepanChakravarthiPadmanabhan
* M.Sc Deebul Nair                - https://github.com/deebuls


Distributed under the MPL license. See ``LICENSE`` for more information.


