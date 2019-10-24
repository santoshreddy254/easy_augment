#!/bin/sh
if [ -d "augmented" ]; then
  # Control will enter here if $DIRECTORY exists.
  rm -R augmented
  mkdir augmented && mkdir augmented/images && mkdir augmented/labels && mkdir augmented/obj_det_labels
fi
if [ ! -d "augmented" ]; then
  # Control will enter here if $DIRECTORY exists.
  mkdir augmented && mkdir augmented/images && mkdir augmented/labels && mkdir augmented/obj_det_labels
fi
python3 image_resize.py
python3 main.py ./images/ ./semantic_labels/ --backgrounds_path ./backgrounds/ --image_save_path ./augmented/images/ --label_save_path ./augmented/labels/ --save_obj_det_label True --obj_det_save_path ./augmented/obj_det_labels/ --num_images $1 --max_objects 3 --real_img_type .png
