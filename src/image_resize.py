import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
import glob

print("resizing images and semantic lables")
files = glob.glob("images_and_jsons/*.jpg")
for f in files:
    img = cv2.imread(f)
    res = cv2.resize(img, (640, 480))
    name = f.split('/')[-1].split('.')[0]
    cv2.imwrite('images/'+name+'.png', res)

files = glob.glob("semantic_labels/*.png")
for f in files:
    img = cv2.imread(f)
    res = cv2.resize(img, (640, 480))
    name = f.split('/')[-1].split('.')[0]
    cv2.imwrite('semantic_labels/'+name+'.png', res)
