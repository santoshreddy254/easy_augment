
import os
import logging
import cv2
from easy_augment.utils.populate_src import populate_source
import numpy as np


def fetch_background_images(generator_options):
    """
    :return: Returns a list of background images.
    :raises: Warning if background does not have the required dimension.
            The background is then resized.
    """
    backgrounds_path = generator_options.get_backgrounds_path()
    background_files = os.listdir(backgrounds_path)
    background_files = [os.path.join(backgrounds_path, file)
                        for file in background_files]

    background_imgs = list()
    for file in background_files:
        img = cv2.imread(file)
        if list(img.shape[0:2]) != generator_options.get_image_dimension():
            logging.warning('Background dimension {} not expected'.format(
                img.shape))
            logging.warning('Rescaling background to shape: {}'.format(
                tuple(generator_options.get_image_dimension() + [3])))
            img = cv2.resize(img, tuple(reversed(
                generator_options.get_image_dimension())))

        background_imgs.append(img)

    return background_imgs


def fetch_image_gt_paths(generator_options):
    """
    Mode 1 (Generation):
    This function counts the number of annotated images and
    fetches the path of the images and corresponding labels.

    :return: files_counter: The number of images read.
             object_files_dict: A dictionary which maps object names
                                to corresponding image and label paths.

    Mode 2 (Save visuals):
    This function creates a list containing lists of image path, semantic
    label path and object detection path.
    :return: data_paths list.
    """
    if generator_options.get_src_label_path() is not None:
        populate_source()
    if generator_options.get_mode() == 1:
        object_files_dict = dict()
        files_counter = 0

        for item in os.listdir(generator_options.get_label_path()):
            cls_path = os.path.join(generator_options.get_label_path(), item)
            if os.path.isdir(cls_path):
                obj_files = list()
                for files in sorted(os.listdir(cls_path)):
                    files_counter += 1
                    obj_files.append([os.path.join(
                        generator_options.get_image_path(), item,
                        files.split('.')[0] + generator_options.get_image_type()),
                        os.path.join(generator_options.get_label_path(), item, files)])

                    object_files_dict[item] = obj_files.copy()
            else:
                files_counter += 1
                cls_name = '_'.join(item.split('_')[:-1])
                if object_files_dict.get(cls_name, None) is None:
                    object_files_dict[cls_name] = list()
                object_files_dict[cls_name].append([os.path.join(
                    generator_options.get_image_path(),
                    item.split('.')[0] + generator_options.get_image_type()),
                    os.path.join(generator_options.get_label_path(), item)])

        return files_counter, object_files_dict

    else:
        data_paths = []
        for label_files in sorted(os.listdir(generator_options.get_label_path())):
            img_path = os.path.join(generator_options.get_image_path(),
                                    label_files.split('.')[0] +
                                    generator_options.get_image_type())
            label_path = os.path.join(generator_options.get_label_path(),
                                      label_files)
            data_paths.append([img_path, label_path])

        return data_paths


def read_image_labels(object_files_dict, generator_options):
    """

    :param object_files_dict: A dictionary which maps object names
                                to corresponding image and label paths.
    :return: A dictionary which maps object names to corresponding
             image and label data.
    """
    LABEL_TO_CLASS, CLASS_TO_LABEL, _ = generator_options.generate_label_to_class()
    class_name_to_data_dict = {}
    for key in CLASS_TO_LABEL:
        if key is not 'background':
            data_list = object_files_dict.get(key, None)
            class_name_to_data_dict[key] = list()
            if data_list is not None:
                for data in data_list:
                    img = cv2.imread(data[0])
                    # img = img + np.round(np.random.random(img.shape))
                    img = img + np.random.randint(-15, 15, size=img.shape,
                                                  dtype=np.int8)
                    img = np.clip(img, 0, 255)
                    label = cv2.imread(data[1], 0)
                    class_name_to_data_dict[key].append([img, label])

    return class_name_to_data_dict
