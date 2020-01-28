# from arguments import generator_options
from easy_augment.utils.get_backgrounds_and_data import fetch_background_images
import numpy as np
import random
from scipy.spatial.distance import cdist


def remove_clutter(objects_list, augmenter_list, regenerate_count, image_dimension, generator_options):
    """
    This function removes elements from the augmenter list which have
    objects occupy an area in image space larger than "max_occupied_area"
    or have objects which are too close to each other determined my
    "min_distance".

    :param objects_list: List containing details of all objects.
    :param augmenter_list: Augmenter list containing details regarding the
                            artificial image.
    :param regenerate_count: Count of attempts already made to create new
                            elements for augmenter list.
    :return: No returns.
    """
    removed_vectors = 0
    for index, vector in enumerate(augmenter_list):
        vector_area = 0
        for i in range(vector['num_objects_to_place']):
            vector_area += objects_list[vector['what_objects'][i]]['obj_area']
        dist_btw_locations = cdist(vector['locations'], vector['locations'])
        np.fill_diagonal(dist_btw_locations, np.inf)

        if (vector_area > np.product(generator_options.get_image_dimension())
                * generator_options.get_max_occupied_area() or
                np.any(dist_btw_locations < generator_options.get_min_distance())):
            del augmenter_list[index]
            removed_vectors += 1

    if (regenerate_count < generator_options.get_num_regenerate()
            and removed_vectors is not 0):
        regenerate_count += 1
        create_augmenter_list(objects_list, image_dimension, generator_options, is_regeneration=True,
                              removed_elements=removed_vectors,
                              regenerate_count=regenerate_count,
                              augmenter_list=augmenter_list)


def get_random_locations(num_random_locations, image_dimension):
    """
    :param num_random_locations: Number of random locations in pixel space.
    :return: A list of random (x,y) locations in pixel space.
    """

    location = [[random.randrange(0, image_dimension[0], 120), random.randrange(0, image_dimension[1], 120)]
                for _ in range(num_random_locations)]
    return np.array(location)


def create_augmenter_list(objects_list, image_dimension, generator_options, is_regeneration=False, removed_elements=None,
                          regenerate_count=None, augmenter_list=None):
    """
    :param objects_list: List containing details of all objects.
    :param is_regeneration: Currently regenerate elements or create new
                            list of elements.
    :param removed_elements: How many elements have been removed and needs
                            to be regenerated.
    :param regenerate_count: How many regeneration attempts have already
                            been made.
    :param augmenter_list: A list of elements where each element is a dictionary
                            containing the following details regarding the artificial
                            image:
                            1. 'background_image': The background image to use.
                            2. 'num_objects_to_place': Number of objects to be placed.
                            3. 'what_objects': A list of indexes indication what objects
                                                need to be placed.
                            4. 'locations': A list of coordinates in the image where
                                            each object needs to be placed.
    :return: The generated augmenter list.
    """
    objects_index = np.arange(0, len(objects_list))
    background_images = fetch_background_images(generator_options)
    if is_regeneration:
        augmenter_list = augmenter_list
        num_images = removed_elements
        regenerate_count = regenerate_count
    else:
        augmenter_list = []
        num_images = generator_options.get_num_images()
        regenerate_count = 0
    for i in range(num_images):
        num_objects_to_place = np.random.randint(1,
                                                 high=generator_options.get_max_objects())
        what_objects = [objects_index[i] for i in range(num_objects_to_place)]

        if i % len(background_images) == 0:
            np.random.shuffle(background_images)

        np.random.shuffle(objects_index)

        augmenter_list.append({'background_image': background_images[
            i % len(background_images)],
            'num_objects_to_place': num_objects_to_place,
            'what_objects': what_objects,
            'locations': get_random_locations(num_objects_to_place, image_dimension)})

    if generator_options.get_remove_clutter():
        remove_clutter(objects_list, augmenter_list,
                       regenerate_count, image_dimension, generator_options)

    return augmenter_list
