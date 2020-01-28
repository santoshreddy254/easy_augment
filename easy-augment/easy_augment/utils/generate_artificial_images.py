# from arguments import generator_options
from easy_augment.utils.object_details import get_scaled_objects
from easy_augment.utils.generate_augmenter_list import create_augmenter_list
from easy_augment.utils.saver import make_save_dirs
from easy_augment.utils.saver import save_data
import copy
import numpy as np
import tqdm
from joblib import Parallel, delayed
import multiprocessing


def get_locations_in_image(obj_locations, generator_options):
    """
    :param obj_locations: List of (x,y) locations.
    :return: array of locations within the image space.
    """
    locs_within_image = []
    for index, location in enumerate(obj_locations):
        if (0 <= location[0] <= generator_options.get_image_dimension()[0]
                and 0 <= location[1] <= generator_options.get_image_dimension()[1]):
            locs_within_image.append(location)

    return np.array(locs_within_image)


def get_augmented_image(original_image, original_label,
                        obj_details, location, generator_options):
    """
    This function gets an image, label and object details and returns
    a new image and label with the object placed.

    :param original_image: The image on which an object needs to be placed.
    :param original_label: The corresponding label image.
    :param obj_details: The details dictionary of the object to be placed.
    :param location: The location in pixel coordinates where the object
                     needs to be placed.
    :return: returns image and label augmented with the object to be placed.
    """

    augmented_image = original_image.copy()
    augmented_label = original_label.copy()
    obj_details_to_augment = copy.deepcopy(obj_details)
    min_loc_index = np.argmin(np.sum(
        obj_details_to_augment['obj_loc'], axis=1))
    obj_details_to_augment['obj_loc'] -= (obj_details_to_augment['obj_loc'][
                                          min_loc_index, :] - location)

    for index, loc in enumerate(obj_details_to_augment['obj_loc']):
        if (0 < loc[0] < augmented_image.shape[0]
                and 0 < loc[1] < augmented_image.shape[1]):
            augmented_image[tuple(loc)] = obj_details_to_augment[
                'obj_vals'][index]
            augmented_label[tuple(loc)] = obj_details_to_augment[
                'label_vals'][index]

    if generator_options.get_save_obj_det_label():
        obj_locations = get_locations_in_image(
            obj_details_to_augment['obj_loc'], generator_options)
        rect_points = [min(obj_locations[:, 1]), min(obj_locations[:, 0]),
                       max(obj_locations[:, 1]), max(obj_locations[:, 0])]

        obj_det_label = [obj_details_to_augment['obj_name']] + rect_points
        return augmented_image, augmented_label, obj_det_label

    return augmented_image, augmented_label


def worker(objects_list, index, element, obj_det_label, background_label, generator_options):
    """
    This is a worker function created for parallel processing
     of "perform_augmentation" function.
    :param objects_list: List containing details of all objects.
    :param index: The index of the current element.
    :param element: The current element in the augment vector.
    :param obj_det_label: Object detection label.
    :param background_label: A 1 channel image filled with
                             background label value.
    :return: No returns.
    """
    artificial_image = element['background_image']
    semantic_label = background_label.copy()
    obj_det_label.clear()
    obj_details_list = [objects_list[this_object]
                        for this_object in element['what_objects']]
    obj_details_list = sorted(obj_details_list,
                              key=lambda k: k['obj_area'],
                              reverse=True)
    for i in range(element['num_objects_to_place']):
        if generator_options.get_save_obj_det_label():
            artificial_image, semantic_label, rect_label = (
                get_augmented_image(artificial_image,
                                    semantic_label,
                                    obj_details_list[i],
                                    element['locations'][i], generator_options))
            obj_det_label.append(rect_label)
        else:
            artificial_image, semantic_label = (
                get_augmented_image(artificial_image,
                                    semantic_label,
                                    obj_details_list[i],
                                    element['locations'][i], generator_options))
    save_data(artificial_image, semantic_label, obj_det_label, index, generator_options)


def perform_augmentation(generator_options):
    """

    This function goes through the augmenter list and generates an artificial
    image for each element in the augmenter list. The results are saved in the
    corresponding locations specified by "generator_options".

    In each element of augmenter list, objects in 'what_objects' is taken and
    pasted on top of the 'background_image' in the element...
    :return: No returns.
    """
    _, CLASS_TO_LABEL, _ = generator_options.generate_label_to_class()
    make_save_dirs(generator_options)
    objects_list = get_scaled_objects(generator_options)
    augmenter_list = create_augmenter_list(
        objects_list, generator_options.get_image_dimension(), generator_options)
    obj_det_label = list()
    background_label = np.ones(tuple(
        generator_options.get_image_dimension())) * (
        CLASS_TO_LABEL['background'])

    num_cores = multiprocessing.cpu_count()
    Parallel(n_jobs=num_cores)(delayed(worker)(objects_list, index,
                                               element, obj_det_label, background_label, generator_options)
                               for index, element in enumerate(tqdm.tqdm(
                                   augmenter_list,
                                   desc='Generating artificial images')))
    return True
