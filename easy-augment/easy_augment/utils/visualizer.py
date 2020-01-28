# from arguments import generator_options
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np


# http://phrogz.net/css/distinct-colors.html
colormap = [[128, 128, 128], [127, 0, 0], [51, 13, 13], [140, 70, 70],
            [217, 76, 54], [230, 180, 172], [102, 80, 77], [242, 97, 0],
            [115, 61, 0], [242, 157, 61], [64, 41, 16], [204, 180, 153],
            [255, 204, 0], [140, 131, 0], [76, 74, 38], [217, 213, 163],
            [206, 242, 61], [48, 51, 38], [70, 128, 32], [7, 51, 0],
            [120, 153, 115], [0, 255, 34], [127, 255, 145], [128, 255, 229],
            [0, 51, 48], [38, 145, 153], [64, 217, 255], [182, 230, 242],
            [0, 60, 89], [102, 156, 204], [0, 36, 89], [80, 57, 230],
            [108, 96, 191], [20, 0, 77], [195, 57, 230], [182, 143, 191],
            [51, 26, 49], [89, 67, 88], [115, 0, 77], [242, 61, 182],
            [166, 83, 116], [255, 64, 115], [51, 38, 42]]

colormap = np.asarray([list(reversed(rgb)) for rgb in colormap],
                      dtype=np.uint8)


def plot_preview(image, label, obj_det_label, index, generator_options):
    """
    This function can be used to plot a preview image,
    which shows the image and labels alongside each other.
    :param image: Image to plot.
    :param label: Corresponding segmentation label.
    :param obj_det_label: Corresponding object detection label.
                          Can be None.
    :param index: The index number of the image.
    :return: Nothing is returned.
    """
    _, CLASS_TO_LABEL, _ = generator_options.generate_label_to_class()
    label = label.copy()

    figure = plt.figure()
    figure.set_figheight(15)
    figure.set_figwidth(20)
    figure.add_subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.xticks([])
    plt.yticks([])

    figure.add_subplot(1, 2, 2)

    if obj_det_label is not None:
        objects_in_image = ['background']
        for l in obj_det_label:
            box_value = CLASS_TO_LABEL[l[0]]
            for i in range(l[1], l[3] + 1):
                if i < generator_options.image_dimension[0]:
                    label[i, l[2]:l[2] + 3] = box_value
                    label[i, l[4] - 3:l[4]] = box_value

            for i in range(l[2], l[4] + 1):
                if i < generator_options.image_dimension[1]:
                    label[l[1]:l[1] + 3, i] = box_value
                    label[l[3] - 3:l[3], i] = box_value
            objects_in_image.append(l[0])

        unique_objects = sorted(np.unique(objects_in_image),
                                key=lambda k: len(k))
        [plt.plot(0, 0, '-', c=np.flip(colormap[
            CLASS_TO_LABEL[obj]], 0) / 255.,
            label=obj)
         for obj in unique_objects]

        leg = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102),
                         loc=3, ncol=2, mode="expand",
                         borderaxespad=0., prop={'size': 20})

        for handle, line, text in zip(leg.legendHandles,
                                      leg.get_lines(), leg.get_texts()):
            handle.set_linewidth(15)
            text.set_color(line.get_color())

    mask = colormap[np.array(label, dtype=np.uint8)]
    plt.imshow(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB))
    plt.xticks([])
    plt.yticks([])

    save_path = os.path.join(
        generator_options.preview_save_path,
        generator_options.name_format %
        (index + generator_options.start_index) + '.png')
    plt.savefig(save_path, bbox_inches="tight")
    plt.close(figure)


def save_overlay(image, label, index, generator_options):
    """
    This function overlays the segmentation label on the image and
    saves the resultant image.
    :param image: Image to be overlaid.
    :param label: Label to overlay.
    :param index: Index to be appended to save file name.
    :return: No returns.
    """
    image = image.copy()
    label = label.copy()
    mask = colormap[np.array(label, dtype=np.uint8)]

    alpha = generator_options.get_overlay_opacity()
    cv2.addWeighted(mask, alpha, image, 1 - alpha,
                    0, image)
    save_path = os.path.join(
        generator_options.overlay_save_path,
        generator_options.name_format %
        (index + generator_options.start_index) + '.png')
    cv2.imwrite(save_path, image)


def save_visuals(image, label, obj_det_label, index, generator_options):
    """
    This function saves the mask if generator option requires
    mask saving. Also calls preview plotting and saving image
    overlay based on generator options.
    :param image: The image whose labels are to be visualized.
    :param label: The corresponding semantic labels.
    :param obj_det_label: The corresponding object detection labels.
    :param index: Index to be appended to save file name.
    :return: No returns.
    """
    if generator_options.save_mask:
        cv2.imwrite(os.path.join(
            generator_options.mask_save_path,
            generator_options.name_format %
            (index + generator_options.start_index) + '.png'),
            colormap[np.array(label, dtype=np.uint8)])

    if generator_options.save_label_preview:
        plot_preview(image, label, obj_det_label, index, generator_options)

    if generator_options.save_overlay:
        save_overlay(image, label, index, generator_options)
