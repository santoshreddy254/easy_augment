
# Easy Augmentor


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
4) libpcl-dev==1.7
5) python 3.5

## Limitations
1) Number of classes captured should be more than or equal to 2.

## Installation

Linux:

```sh
pip3 install easy-augmentor
```



## Release History


* 1.0.0
    * First release for crowd testing
* 1.1.0
    * Now user can save RGB, pointcloud, depth, boundingbox, semantic label
    * Continous mode added

## Contributors
* Santosh Muthireddy              – https://github.com/santoshreddy254
* Naresh Kumar Gurulingan         - https://github.com/NareshGuru77
* Deepan Chakravarthi Padmanabhan - https://github.com/DeepanChakravarthiPadmanabhan
* M.Sc Deebul Nair                - https://github.com/deebuls


Distributed under the MLP license. See ``LICENSE`` for more information.


