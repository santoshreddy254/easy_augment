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
python3 gui_main.py
