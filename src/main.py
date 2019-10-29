# import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from arguments import generator_options
from generate_artificial_images import perform_augmentation
from visualizer import save_visuals
from saver import make_save_dirs
from get_backgrounds_and_data import fetch_image_gt_paths
from object_details import find_obj_loc_and_vals
from generate_artificial_images import get_locations_in_image
import cv2
import tqdm
from joblib import Parallel, delayed
import multiprocessing
import os
import numpy as np
from pascal_voc_writer import Writer


def read_files_and_visualize(data_p):
    """
    This function reads all the images and corresponding
    labels and calls the visualizer.
    :param data_p: List containing paths to images and labels
    :return: No returns.
    """

    image = cv2.imread(data_p[0])
    label = cv2.imread(data_p[1], 0)
    name = data_p[1].split('/')[-1].split('.')[0]
    obj_name = name[:-4]
    label_value = sorted(np.unique(label))[0]
    obj_details = find_obj_loc_and_vals(image, label,
                                        label_value, obj_name)
    obj_locations = get_locations_in_image(obj_details['obj_loc'])
    rect_points = [min(obj_locations[:, 1]), min(obj_locations[:, 0]),
                   max(obj_locations[:, 1]), max(obj_locations[:, 0])]
    obj_label = [[obj_name] + rect_points]
    save_visuals(image, label, obj_label, name)

    if generator_options.save_obj_det_label:
        img_path = data_p[0]
        img_dimension = generator_options.image_dimension
        writer = Writer(img_path, img_dimension[1],
                        img_dimension[0])
        [writer.addObject(*l) for l in obj_label]
        save_path = os.path.join(
            generator_options.obj_det_save_path,
            generator_options.name_format %
            name + '.xml')
        writer.save(save_path)


if __name__ == '__main__':

    if generator_options.mode == 1:
        perform_augmentation()
    else:
        make_save_dirs()
        data_paths = fetch_image_gt_paths()
        num_cores = multiprocessing.cpu_count()
        Parallel(n_jobs=num_cores)(delayed(read_files_and_visualize)(p)
                                   for p in tqdm.tqdm(
            data_paths, desc='Saving visuals'))
