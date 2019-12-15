
# Realsense Augmentor

[![Build Status](https://travis-ci.org/santoshreddy254/Data_Augmentor_With_GUI.svg?branch=master)](https://travis-ci.org/santoshreddy254/Data_Augmentor_With_GUI)

> End to end software to capture new objects using RGBD camera and augment them to get a annotated dataset to train deep nets

1) Pipeline to artificial generate annotated data for training deep learning models.
2) Pipeline includes starting from capturing images using provided camera (Realsense),
generate semantic labels of the captured image and then generate the artificial images.
3) GUI required for the end user from capturing to labelling and generating new data.

![](header.png)
## Requirements
1) Ubuntu 16.04 or higher
2) Intel Realsense Camera
3) Processer intel i5 or higher
4) Ram ?
5) python3

## Limitations
1) Number of classes captured should be more than or equal to 2.

## Installation

Linux:

```sh
git clone https://github.com/santoshreddy254/realsense_augmentor.git
cd realsense_augmentor
./setup.sh
```


## Usage example

```sh
cd realsense_augmentor
python3 src/Start_gui.py
```
1) Start page will be as below and select the path to save the captured images.
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/window_01.png)
2) Next window will have image and mask of corresponding object. Capture as many as images per classe.
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/window_02-1.png)
3) Click add to add new class label.
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/window_02-2.png)
4) Click save to save the current displyed image and semantic label.
5) Click finish once done with capturing all the images.
6) Folder name \textbf{captured_data} in selected save path will have images, labels and labels.txt
6) Input parameters to generate artificial images need to be filled next window.
![alt text](https://github.com/santoshreddy254/realsense_augmentor/blob/master/src/data/window_03.png)
7) Click OK once setting up the parameters.
8) Folder name \textbf{augmented} in selected save path will have artificial images.


## Release History


* 1.0.0
    * First release for crowd testing

## Meta

Santosh Muthireddy – santoshreddy45@yahoo.com

Distributed under the MLP license. See ``LICENSE`` for more information.


