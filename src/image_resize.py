import cv2
import numpy as np
import glob

def resize_images(folder_path,image_dimension):
    print("resizing images")
    files = glob.glob(folder_path+'/*')
    for f in files:
        img = cv2.imread(f)
        res = cv2.resize(img, (image_dimension[1], image_dimension[0]))
        name = f.split('/')[-1].split('.')[0]
        extension = f.split('/')[-1]
        cv2.imwrite(folder_path+'/'+extension, res)
