import cv2
import numpy as np
import glob
import os


def resize_images(folder_path, image_dimension):
    extensions = ("*.png", "*.jpg", "*.jpeg",)
    files = []
    for extension in extensions:
        files.extend(glob.glob(folder_path+"/"+extension))
    for f in files:
        img = cv2.imread(f)
        res = cv2.resize(img, (image_dimension[1], image_dimension[0]))
        name = f.split('/')[-1].split('.')[0]
        extension = f.split('/')[-1]
        cv2.imwrite(folder_path+'/temp/'+extension, res)


def rename_images_labels(labels_folder, images_folder, labels_file_path):
    labels = ['background']
    labels_txt_file = open(labels_file_path)
    for i in labels_txt_file.readlines():
        if i.rstrip()not in['__ignore__', '_background_']:
            labels.append(i.rstrip())
    images_files = glob.glob(images_folder+"*")
    images_files.sort()
    labels_files = glob.glob(labels_folder+"*")
    labels_files.sort()
    class_count = np.zeros(len(labels)).astype(np.float)
    for i, j in zip(images_files, labels_files):
        label_image = cv2.imread(j)
        head, tail = os.path.split(i)
        class_count[np.max(label_image)] += 1
        new_name = labels[np.max(label_image)]+"_" + \
            "%04d" % class_count[np.max(label_image)]+"."+tail.split('.')[-1]
        os.rename(i, head+"/"+new_name)
        os.rename(j, os.path.split(j)[0]+"/"+new_name)


def rename_backgrounds(backgrounds_folder):
    backgrounds_files = glob.glob(backgrounds_folder+"*")
    for i, j in enumerate(backgrounds_files):
        label_image = cv2.imread(j)
        head, tail = os.path.split(j)
        new_name = "background_" + \
            "%04d" % i+"."+tail.split('.')[-1]
        os.rename(j, head+"/"+new_name)
