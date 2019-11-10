import os
import cv2
import numpy as np
# from arguments import LABEL_TO_CLASS
# from arguments import generator_options

def populate_source():
    import AIG_Window
    generator_options = AIG_Window.get_generator_options()
    LABEL_TO_CLASS, CLASS_TO_LABEL, _ = generator_options.generate_label_to_class()
    src_label_path = generator_options.src_label_path
    src_image_path = generator_options.src_image_path

    src_imgs = sorted([os.path.join(src_image_path, file)
                for file in os.listdir(src_image_path)])
    src_labels = sorted([os.path.join(src_label_path, file)
                  for file in os.listdir(src_label_path)])

    img_count = 1000
    for src_label, src_img in zip(src_labels, src_imgs):
        label = cv2.imread(src_label, 0)
        img = cv2.imread(src_img)
        classes_in_img = np.unique(label)
        for cls in classes_in_img:
            if cls != 0:
                label_copy = label.copy()
                label_copy[label_copy!=cls] = 0
                cv2.imwrite(os.path.join(generator_options.label_path,
                                         LABEL_TO_CLASS[cls] + '_' +
                                         generator_options.name_format %
                                         (img_count) + '.png'), label_copy)
                cv2.imwrite(os.path.join(generator_options.image_path,
                                         LABEL_TO_CLASS[cls] + '_' +
                                         generator_options.name_format %
                                         (img_count) + '.jpg'), img)
                img_count += 1
