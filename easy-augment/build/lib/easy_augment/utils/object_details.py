# from arguments import generator_options
from easy_augment.utils.get_backgrounds_and_data import read_image_labels, \
    fetch_image_gt_paths
import tqdm
import numpy as np
import cv2


def get_num_scales_and_objects(files_count, generator_options):
    """
    This function picks a random number of scales in the range 1 to 5
    for each real image if num_scales is randomize. Else takes num_scales.

    :return: num_scales which is either an array of number of scales or a
             single number of scales.
    """
    if generator_options.get_num_scales() is 'randomize':
        number_of_scales = np.random.randint(
            1, 5,
            size=files_count)
    else:
        number_of_scales = generator_options.get_num_scales()
    return number_of_scales


def find_obj_loc_and_vals(image, label, label_value, obj_name):
    """
    This function creates a dictionary containing details regarding
    an object in an image.

    :param image: Image from which found object needs to be extracted.
    :param label: Label on which object needs to be searched.
    :param label_value: The label value of the object to be searched.
    :param obj_name: The name of the object to be searched.
    :return: returns a dictionary which links:
                1. 'obj_loc' to (x,y) locations of the object obtained using
                    the label definition...
                2. 'obj_vals' to the intensity values of the object in the
                    corresponding 'obj_loc'...
                3. 'label_vals' to an array whose all elements is the value of
                    the object label...
                4. 'obj_name' to the name of the object..
                5. 'rect_points' to the coordinates of the points to obtain
                    bounding rectangle.
                6. 'obj_area' to the area occupied by the object in pixel space.

    """
    obj_loc = np.argwhere(label == label_value)
    obj_vals = [image[tuple(loc)] for loc in obj_loc]
    obj_vals = np.array(obj_vals)
    label_vals = np.ones(len(obj_loc)) * label_value
    rect_points = [min(obj_loc[:, 0]), min(obj_loc[:, 1]),
                   max(obj_loc[:, 0]), max(obj_loc[:, 1])]
    obj_area = (rect_points[2] - rect_points[0]
                ) * (rect_points[3] - rect_points[1])

    return {'obj_loc': obj_loc, 'obj_vals': obj_vals,
            'label_vals': label_vals, 'obj_name': obj_name,
            'rect_points': rect_points, 'obj_area': obj_area}


def get_different_scales(image, image_label, label_value,
                         number_of_scales, obj_name, obj_num, generator_options):
    """
    This functions creates different scales of the object based on the
    number of scales parameter and removes objects which are too small.

    :param image: Image of which different scales needs to be created.
    :param image_label: The corresponding label of the image.
    :param label_value: The label value of the object in the image.
    :param number_of_scales: The number of scales required for the object.
    :param obj_name: The name of the object.
    :param obj_num: Current image number.
    :return: A list of dictionaries containing details of the scaled objects.
    """
    _, CLASS_TO_LABEL, SCALES_RANGE_DICT = generator_options.generate_label_to_class()
    if type(number_of_scales) is np.ndarray:
        num_scales = number_of_scales[obj_num]
        scale_difference = 1.2 / number_of_scales[obj_num]
    else:
        num_scales = number_of_scales
        scale_difference = 1.2 / number_of_scales

    zoom_range = SCALES_RANGE_DICT[obj_name]
    if zoom_range is None:
        scales = [i * scale_difference for i in range(1, num_scales + 1)]
    else:
        scales = np.linspace(zoom_range[0], zoom_range[1],
                             num=num_scales)

    scaled_objects = list()
    for i in range(0, num_scales):
        scaled_objects.append(find_obj_loc_and_vals(
            cv2.resize(image, (0, 0), fx=scales[i], fy=scales[i]),
            cv2.resize(image_label, (0, 0), fx=scales[i], fy=scales[i]),
            label_value, obj_name))

    # Not needed it might effect for smaller objects in a given image

    # image_area = np.product(generator_options.get_image_dimension())
    # for index, obj in enumerate(scaled_objects):
    #     print(obj['obj_area'], generator_options.get_min_obj_area() / 100. *
    #           image_area, generator_options.get_max_obj_area() / 100. * image_area, image_area)
    #     if not (generator_options.get_min_obj_area() / 100. * image_area
    #             < obj['obj_area'] <
    #             generator_options.get_max_obj_area() / 100. * image_area):
    #         del scaled_objects[index]

    return scaled_objects


def get_scaled_objects(generator_options):
    """
    This function returns a list of details of all objects.

    :return: A list of dictionaries containing details of all the scaled objects.
    """
    _, CLASS_TO_LABEL, SCALES_RANGE_DICT = generator_options.generate_label_to_class()
    objects_list = list()
    obj_num = -1

    files_count, object_files = fetch_image_gt_paths(generator_options)
    number_of_scales = get_num_scales_and_objects(files_count, generator_options)
    class_name_to_data = read_image_labels(object_files, generator_options)
    for key in tqdm.tqdm(CLASS_TO_LABEL,
                         desc='Loading images and labels class by class'):
        if key is not 'background':
            data_list = class_name_to_data[key]
            for data in data_list:
                obj_num += 1
                objects_list += get_different_scales(data[0],
                                                     data[1],
                                                     CLASS_TO_LABEL[key],
                                                     number_of_scales,
                                                     key, obj_num, generator_options)

    return objects_list
