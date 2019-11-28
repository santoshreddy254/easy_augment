import argparse
import collections
import copy


class GeneratorOptions():
    def __init__(self):
        self.mode = 1
        self.image_dimension = [480, 640]
        self.num_scales = 1
        self.backgrounds_path = ''
        self.image_path = ''
        self.label_path = ''
        self.src_image_path = None
        self.src_label_path = None
        self.obj_det_save_path = ''
        self.real_img_type = '.png'
        self.min_obj_area = 2
        self.max_obj_area = 700
        self.save_label_preview = False
        self.obj_det_save_path = None
        self.save_mask = False
        self.save_overlay = False
        self.overlay_opacity = 0.6
        self.image_save_path = ''
        self.label_save_path = ''
        self.preview_save_path = None
        self.obj_det_save_path = None
        self.mask_save_path = None
        self.overlay_save_path = None
        self.start_index = 0
        self.name_format = '%05d'
        self.remove_clutter = True
        self.num_images = 20
        self.max_objects = 3
        self.num_regenerate = 100
        self.min_distance = 100
        self.max_occupied_area = 0.8
        self.save_obj_det_label = False
        self.labels_file_path = ''

    def set_labels_file_path(self, labels_file_path):
        self.labels_file_path = labels_file_path

    def get_labels_file_path(self):
        return self.labels_file_path

    def generate_label_to_class(self):
        self.labels = ['background']
        self.LABEL_TO_CLASS = dict()
        self.SCALES_RANGE_DICT = dict()
        self.labels_file = open(self.labels_file_path)
        for i in self.labels_file.readlines():
            if i.rstrip()not in['__ignore__', '_background_']:
                self.labels.append(i.rstrip())

        for i, j in enumerate(self.labels):
            self.LABEL_TO_CLASS[i] = j
            if j not in ['background']:
                self.SCALES_RANGE_DICT[j] = None

        self.CLASS_TO_LABEL = {value: key for key, value in self.LABEL_TO_CLASS.items()}

        return self.LABEL_TO_CLASS, self.CLASS_TO_LABEL, self.SCALES_RANGE_DICT

    def set_max_occupied_area(self, max_occupied_area):
        self.max_occupied_area = max_occupied_area

    def get_max_occupied_area(self):
        return self.max_occupied_area

    def set_min_distance(self, min_distance):
        self.min_distance = min_distance

    def get_min_distance(self):
        return self.min_distance

    def set_num_regenerate(self, num_regenerate):
        self.num_regenerate = num_regenerate

    def get_num_regenerate(self):
        return self.num_regenerate

    def set_remove_clutter(self, remove_clutter):
        self.remove_clutter = remove_clutter

    def get_remove_clutter(self):
        return self.remove_clutter

    def set_name_format(self, name_format):
        self.start_index = name_format

    def get_name_format(self):
        return self.name_format

    def set_start_index(self, start_index):
        self.start_index = start_index

    def get_start_index(self):
        return self.start_index

    def set_overlay_save_path(self, overlay_save_path):
        self.mask_save_path = overlay_save_path

    def get_overlay_save_path(self):
        return self.overlay_save_path

    def set_mask_save_path(self, mask_save_path):
        self.mask_save_path = mask_save_path

    def get_mask_save_path(self):
        return self.mask_save_path

    def set_preview_save_path(self, preview_save_path):
        self.preview_save_path = preview_save_path

    def get_preview_save_path(self):
        return self.preview_save_path

    def set_label_save_path(self, label_save_path):
        self.label_save_path = label_save_path

    def get_label_save_path(self):
        return self.label_save_path

    def set_image_save_path(self, image_save_path):
        self.image_save_path = image_save_path

    def get_image_save_path(self):
        return self.image_save_path

    def set_overlay_opacity(self, overlay_opacity):
        self.overlay_opacity = overlay_opacity

    def get_overlay_opacity(self):
        return self.overlay_opacity

    def set_save_overlay(self, save_overlay):
        self.save_overlay = save_overlay

    def get_save_overlay(self):
        return self.save_overlay

    def set_save_mask(self, save_mask):
        self.save_mask = save_mask

    def get_save_mask(self):
        return self.save_mask

    def set_save_label_preview(self, save_label_preview):
        self.save_label_preview = save_label_preview

    def get_save_label_preview(self):
        return self.save_label_preview

    def set_max_obj_area(self, max_obj_area):
        self.max_obj_area = max_obj_area

    def get_max_obj_area(self):
        return self.max_obj_area

    def set_min_obj_area(self, min_obj_area):
        self.min_obj_area = min_obj_area

    def get_min_obj_area(self):
        return self.min_obj_area

    def set_src_label_path(self, src_label_path):
        self.src_label_path = src_label_path

    def get_src_label_path(self):
        return self.src_label_path

    def set_src_image_path(self, src_image_path):
        self.src_image_path = src_image_path

    def get_src_image_path(self):
        return self.src_image_path

    def set_num_scale(self, num_scales):
        self.num_scales = num_scales

    def get_num_scales(self):
        return self.num_scales

    def set_mode(self, mode):
        self.mode = mode

    def get_mode(self):
        return self.mode

    def set_num_images(self, num_images):
        self.num_images = num_images

    def get_num_images(self):
        return self.num_images

    def set_image_type(self, image_type):
        self.real_img_type = image_type

    def get_image_type(self):
        return self.real_img_type

    def set_max_objects(self, max_objects=3):
        self.max_objects = max_objects

    def get_max_objects(self):
        return self.max_objects

    def set_image_path(self, image_path):
        self.image_path = image_path

    def get_image_path(self):
        return self.image_path

    def set_label_path(self, label_path):
        self.label_path = label_path

    def get_label_path(self):
        return self.label_path

    def get_backgrounds_path(self):
        return self.backgrounds_path

    def set_backgrounds_path(self, backgrouds_path):
        self.backgrounds_path = backgrouds_path

    def set_image_dimension(self, image_dimension):
        self.image_dimension = image_dimension

    def get_image_dimension(self):
        return self.image_dimension

    def set_save_obj_det_label(self, save_flag):
        self.save_obj_det_label = copy.deepcopy(save_flag)

    def get_save_obj_det_label(self):
        return self.save_obj_det_label

    def set_obj_det_save_path(self, obj_det_save_path):
        self.obj_det_save_path = obj_det_save_path

    def get_obj_det_save_path(self):
        return self.obj_det_save_path


# generator_options = GeneratorOptions()
