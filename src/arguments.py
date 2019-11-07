import argparse
import collections
import copy

# Generating LABEL_TO_CLASS, CLASS_TO_LABEL, SCALES_RANGE_DICT based on labels.txt provided
label_file_path = './labels.txt'
labels_file = open(label_file_path)
labels = ['background']
LABEL_TO_CLASS = dict()
SCALES_RANGE_DICT = dict()
for i in labels_file.readlines():
	if i.rstrip()not in['__ignore__','_background_']:
		labels.append(i.rstrip())

for i,j in enumerate(labels):
	LABEL_TO_CLASS[i] = j
	if j not in ['background']:
		SCALES_RANGE_DICT[j] = None

CLASS_TO_LABEL = {value: key for key, value in LABEL_TO_CLASS.items()}

class StoreScalesDict(argparse.Action):
    def __call__(self, parser_scales, namespace, arg_vals, option_string=None):

        for items in arg_vals.split(';'):
            key, value = items.split('=')

            if not any(key == object_key
                       for object_key in list(SCALES_RANGE_DICT.keys())):
                parser_scales.error('Object {} is not recognized.'.format(key))

            value = value.split(',')
            SCALES_RANGE_DICT[key] = [float(v) for v in value]
        setattr(namespace, self.dest, SCALES_RANGE_DICT)


parser = argparse.ArgumentParser(
    description='Arguments to control artificial image generation.')

# parser.add_argument('--mode', default=1, type=int, required=False,
#                     help='1: Generate artificial images; 2: Save visuals.')

parser.add_argument('--image_dimension', default=[480, 640], type=list, required=False,
                    help='Dimension of the real images.')

parser.add_argument('--num_scales', default='randomize', type=str, required=False,
                    help='Number of scales including original object scale.')

parser.add_argument('--backgrounds_path', default='./backgrounds/', type=str, required=False,
                    help='Path to directory where the background images are located.')

parser.add_argument('--image_path',type=str,
                    help='Path to directory where real images are located.')

parser.add_argument('--label_path',type=str,
                    help='Path to directory where labels are located.')

parser.add_argument('--src_image_path', default=None, type=str, required=False,
                    help='Path to directory where real images with multiple objects are located.')

parser.add_argument('--src_label_path', default=None, type=str, required=False,
                    help='Path to directory where labels of images with multiple objects are located.')

parser.add_argument('--obj_det_label_path', type=str, required=False,
                    help='Path to directory where the object detection csv labels are located.')

parser.add_argument('--real_img_type', default='.png', type=str, required=False,
                    help='The format of the real image.')

parser.add_argument('--min_obj_area', default=20, type=int, required=False,
                    help='Minimum area in percentage allowed for an object in image space.')

parser.add_argument('--max_obj_area', default=70, type=int, required=False,
                    help='Maximum area in percentage allowed for an object in image space.')

parser.add_argument('--save_label_preview', default=False, type=bool, required=False,
                    help='Save image+label in single image for preview.')

parser.add_argument('--save_obj_det_label', type=bool, required=False,
                    help='Save object detection labels in csv files.')

parser.add_argument('--save_mask', default=False, type=bool, required=False,
                    help='Save images showing the segmentation mask.')

parser.add_argument('--save_overlay', default=False, type=bool, required=False,
                    help='Save segmentation label overlaid on image.')

parser.add_argument('--overlay_opacity', default=0.6, type=float, required=False,
                    help='Opacity of label on the overlaid image.')

parser.add_argument('--image_save_path', default='./augmented/images/', type=str, required=False,
                    help='Path where the generated artificial image needs to be saved.')

parser.add_argument('--label_save_path', default='./augmented/labels/', type=str, required=False,
                    help='Path where the generated segmentation label needs to be saved.')

parser.add_argument('--preview_save_path', default=None, type=str, required=False,
                    help='Path where object detection labels needs to be saved.')

parser.add_argument('--obj_det_save_path', default=None, type=str, required=False,
                    help='Path where object detection labels needs to be saved.')

parser.add_argument('--mask_save_path', default=None, type=str, required=False,
                    help='Path where segmentation masks needs to be saved.')

parser.add_argument('--overlay_save_path', default=None, type=str, required=False,
                    help='Path where overlaid images needs to be saved.')

parser.add_argument('--start_index', default=None, required=False,
                    help='Index from which image and label names should start.')

parser.add_argument('--name_format', default='%05d', type=str, required=False,
                    help='The format for image file names.')

parser.add_argument('--remove_clutter', default=True, type=bool, required=False,
                    help='Remove images cluttered with objects.')

parser.add_argument('--num_images', default=20,type=int, required=False,
                    help='Number of artificial images to generate.')

parser.add_argument('--max_objects', default=10, type=int, required=False,
                    help='Maximum number of objects allowed in an image.')

parser.add_argument('--num_regenerate', default=100, type=int, required=False,
                    help='Number of regeneration attempts of removed details dict.')

parser.add_argument('--min_distance', default=100, type=int, required=False,
                    help='Minimum pixel distance required between two objects.')

parser.add_argument('--max_occupied_area', default=0.8, type=float, required=False,
                    help='Maximum object occupancy area allowed.')

parser.add_argument('--scale_ranges', dest='SCALES_RANGE_DICT', required=False,
                    action=StoreScalesDict,
                    metavar='Object=min_scale,max_scale;Object=min_scale,max_scale;...',
                    help='Can be used to change the zoom range of specific objects.')


args = parser.parse_args()

if args.save_obj_det_label and args.obj_det_save_path is None:
    parser.error('Path to save object detection labels is also required.')

if args.save_mask and args.mask_save_path is None:
    parser.error('Path to save segmentation masks is also required.')

if args.save_label_preview and args.preview_save_path is None:
    parser.error('Path to save label preview is also required.')

if args.save_overlay and args.overlay_save_path is None:
    parser.error('Path to save overlay is also required.')

if args.start_index is None:
    if list(args.name_format)[-1] == 'd':
        args.start_index = 0
    else:
        args.start_index = ''

if True:
    if args.backgrounds_path is None:
        parser.error('Backgrounds path is also required.')
    if args.image_save_path is None:
        parser.error('Path to save artificial images is also required.')
    if args.label_save_path is None:
        parser.error('Path to save artificial image labels is also required.')


class GeneratorOptions():
	def __init__(self):
		self.mode = 1
	def set_max_occupied_area(self,max_occupied_area):
		args.max_occupied_area = max_occupied_area
	def get_max_occupied_area(self):
		return args.max_occupied_area
	def set_min_distance(self,min_distance):
		args.min_distance = min_distance
	def get_min_distance(self):
		return args.min_distance
	def set_num_regenerate(self,num_regenerate):
		args.num_regenerate = num_regenerate
	def get_num_regenerate(self):
		return args.num_regenerate
	def set_remove_clutter(self,remove_clutter):
		args.remove_clutter = remove_clutter
	def get_remove_clutter(self):
		return args.remove_clutter
	def set_name_format(self,name_format):
		args.start_index = name_format
	def get_name_format(self):
		return args.name_format
	def set_start_index(self,start_index):
		args.start_index = start_index
	def get_start_index(self):
		return args.start_index
	def set_overlay_save_path(self,overlay_save_path):
		args.mask_save_path = overlay_save_path
	def get_overlay_save_path(self):
		return args.overlay_save_path
	def set_mask_save_path(self,mask_save_path):
		args.mask_save_path = mask_save_path
	def get_mask_save_path(self):
		return args.mask_save_path
	def set_preview_save_path(self,preview_save_path):
		args.preview_save_path = preview_save_path
	def get_preview_save_path(self):
		return args.preview_save_path
	def set_label_save_path(self,label_save_path):
		args.label_save_path = label_save_path
	def get_label_save_path(self):
		return args.label_save_path
	def set_image_save_path(self,image_save_path):
		args.image_save_path = image_save_path
	def get_image_save_path(self):
		return args.image_save_path
	def set_overlay_opacity(self,overlay_opacity):
		args.overlay_opacity = overlay_opacity
	def get_overlay_opacity(self):
		return args.overlay_opacity
	def set_save_overlay(self,save_overlay):
		args.save_overlay = save_overlay
	def get_save_overlay(self):
		return args.save_overlay
	def set_save_mask(self,save_mask):
		args.save_mask = save_mask
	def get_save_mask(self):
		return args.save_mask
	def set_save_label_preview(self,save_label_preview):
		args.save_label_preview = save_label_preview
	def get_save_label_preview(self):
		return args.save_label_preview
	def set_max_obj_area(self,max_obj_area):
		args.max_obj_area = max_obj_area
	def get_max_obj_area(self):
		return args.max_obj_area
	def set_min_obj_area(self,min_obj_area):
		args.min_obj_area = min_obj_area
	def get_min_obj_area(self):
		return args.min_obj_area
	def set_src_label_path(self,src_label_path):
		args.src_label_path = src_label_path
	def get_src_label_path(self):
		return args.src_label_path
	def set_src_image_path(self,src_image_path):
		args.src_image_path = src_image_path
	def get_src_image_path(self):
		return args.src_image_path
	def set_num_scale(self,num_scales):
		args.num_scales = num_scales
	def get_num_scales(self):
		return args.num_scales
	def set_mode(self,mode):
		self.mode = mode
	def get_mode(self):
		return self.mode
	def set_num_images(self,num_images):
	    args.num_images = num_images
	def get_num_images(self):
	    return args.num_images
	def set_image_type(self,image_type):
	    args.real_img_type = image_type
	def get_image_type(self):
	    return args.real_img_type
	def set_max_objects(self,max_objects=3):
	    args.max_objects = max_objects
	def get_max_objects(self):
	    return args.max_objects
	def set_image_path(self,image_path):
	    args.image_path = image_path
	def get_image_path(self):
	    return args.image_path
	def set_label_path(self,label_path):
	    args.label_path = label_path
	def get_label_path(self):
	    return args.label_path
	def get_backgrounds_path(self):
	    return args.backgrounds_path
	def set_backgrounds_path(self,backgrouds_path):
	    args.backgrouds_path = backgrouds_path
	def set_image_dimension(self,image_dimension):
		args.image_dimension = image_dimension
	def get_image_dimension(self):
		return args.image_dimension
	def set_save_obj_det_label(self,save_flag):
		# print("setter bool",save_flag)
		args.save_obj_det_label = copy.deepcopy(save_flag)
	def get_save_obj_det_label(self):
		# print("getter bool ",args.save_obj_det_label)
		return args.save_obj_det_label
	def set_obj_det_save_path(self,obj_det_save_path):
		# print("inside setter, ",obj_det_save_path)
		args.obj_det_save_path = obj_det_save_path
	def get_obj_det_save_path(self):
		# print("inside path getter, ", args.obj_det_save_path)
		return args.obj_det_save_path




generator_options = GeneratorOptions()
