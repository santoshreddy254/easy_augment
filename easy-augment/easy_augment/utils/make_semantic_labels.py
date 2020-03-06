import os
import shutil
import numpy as np
import cv2
import glob
import re
import sys


def generate_semantic_labels(input_dir, output_dir_path):
    print("generating semantic labels")
    files = glob.glob(input_dir+"/SegmentationClass/*.npy")
    if os.path.exists(output_dir_path+'/semantic_labels'):
        shutil.rmtree(output_dir_path+'/semantic_labels', ignore_errors=False, onerror=None)
    os.makedirs(output_dir_path+'/semantic_labels')
    for i in files:
        image = np.load(i)
        pat = re.compile(input_dir+'/SegmentationClass/(.*).npy')
        name = re.search(pat, i)
        print(output_dir_path+'/semantic_labels/'+name.group(1)+'.png')
        cv2.imwrite(output_dir_path+'/semantic_labels/'+name.group(1)+'.png', image)
