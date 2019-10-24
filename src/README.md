# Folders
* Please create a folder named images, backgrounds and semantic_labels at root, place images and corresponding semantic labels in this folder, background images in backgrounds folder
* Sample images are placed in those folders
* Folder augmented and internal folders obj_det_labels, images, labels are generated after running artificial_image_generator.sh
* Please place a labels.txt file in root folder and it should look like below 
![alt text](https://github.com/santoshreddy254/artificial_image_generator/blob/master/labels.png)
* Now you can sun ./artificial_image_generator.sh to generate data and that can be found in augmented folder
* --real_img_type .png arg can be changed in ./artificial_image_generator.sh depending on image format we are providing

# Usage:

## Mode 1:
python3 main.py ./images/ ./labels/ --backgrounds_path ./backgrounds/ --image_save_path ./augmented/images/ --label_save_path ./augmented/labels/ --save_label_preview True --preview_save_path ./augmented/preview/ --save_overlay True --overlay_save_path ./augmented/overlay/ --save_obj_det_label True --obj_det_save_path ./augmented/obj_det_labels/ --save_mask True --mask_save_path ./augmented/mask/ --num_images 8

## Mode 2:
python3 main.py ./images/ ./labels/ --backgrounds_path ./backgrounds/ --save_obj_det_label True --obj_det_save_path ./obj_det_labels --mode 2 --name_format %s

# Parameters:
description of arguments could be found in arguments.py
