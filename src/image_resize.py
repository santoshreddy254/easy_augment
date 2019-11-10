import cv2
import numpy as np
import glob

def resize_images(folder_path,image_dimension):
    # files = glob.glob(folder_path+'/*.{jpg,png}',GLOB_BRACE)
    extensions = ("*.png","*.jpg","*.jpeg",)
    files = []
    for extension in extensions:
        files.extend(glob.glob(folder_path+"/"+extension))
    for f in files:
        img = cv2.imread(f)
        res = cv2.resize(img, (image_dimension[1], image_dimension[0]))
        name = f.split('/')[-1].split('.')[0]
        extension = f.split('/')[-1]
        cv2.imwrite(folder_path+'/temp/'+extension, res)
