import pcl
from random import randint
import struct
# Returns Downsampled version of a point cloud
# The bigger the leaf size the less information retained


def do_voxel_grid_filter(point_cloud, LEAF_SIZE=0.01):
    voxel_filter = point_cloud.make_voxel_grid_filter()
    voxel_filter.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
    return voxel_filter.filter()

# Returns only the point cloud information at a specific range of a specific axis


def do_passthrough_filter(point_cloud, name_axis='z', min_axis=0, max_axis=1.0):
    pass_filter = point_cloud.make_passthrough_filter()
    pass_filter.set_filter_field_name(name_axis)
    pass_filter.set_filter_limits(min_axis, max_axis)
    return pass_filter.filter()

# Use RANSAC planse segmentation to separate plane and not plane points
# Returns inliers (plane) and outliers (not plane)


def do_ransac_plane_segmentation(point_cloud, max_distance=0.01):

    segmenter = point_cloud.make_segmenter()

    segmenter.set_model_type(pcl.SACMODEL_PLANE)
    segmenter.set_method_type(pcl.SAC_RANSAC)
    segmenter.set_distance_threshold(max_distance)
    segmenter.set_optimize_coefficients(True)

    # obtain inlier indices and model coefficients
    inlier_indices, coefficients = segmenter.segment()

    inliers = point_cloud.extract(inlier_indices, negative=False)
    outliers = point_cloud.extract(inlier_indices, negative=True)

    return inliers, outliers


def XYZRGB_to_XYZ(XYZRGB_cloud):
    """ Converts a PCL XYZRGB point cloud to an XYZ point cloud (removes color info)

        Args:
            XYZRGB_cloud (PointCloud_PointXYZRGB): A PCL XYZRGB point cloud

        Returns:
            PointCloud_PointXYZ: A PCL XYZ point cloud
    """
    XYZ_cloud = pcl.PointCloud()
    points_list = []

    for data in XYZRGB_cloud:
        points_list.append([data[0], data[1], data[2]])

    XYZ_cloud.from_list(points_list)
    return XYZ_cloud


def get_clusters(cloud, tolerance, min_size, max_size):

    tree = cloud.make_kdtree()
    extraction_object = cloud.make_EuclideanClusterExtraction()

    extraction_object.set_ClusterTolerance(tolerance)
    extraction_object.set_MinClusterSize(min_size)
    extraction_object.set_MaxClusterSize(max_size)
    extraction_object.set_SearchMethod(tree)

    # Get clusters of indices for each cluster of points, each clusterbelongs to the same object
    # 'clusters' is effectively a list of lists, with each list containing indices of the cloud
    clusters = extraction_object.Extract()
    return clusters


# clusters is a list of lists each list containing indices of the cloud
# cloud is an array with each cell having three numbers corresponding to x, y, z position
# Returns list of [x, y, z, color]

def get_colored_clusters(clusters, cloud):

    # Get a random unique colors for each object
    number_of_clusters = len(clusters)
    colors = get_color_list(number_of_clusters)

    colored_points = []

    # Assign a color for each point
    # Points with the same color belong to the same cluster
    for cluster_id, cluster in enumerate(clusters):
        for c, i in enumerate(cluster):
            x, y, z = cloud[i][0], cloud[i][1], cloud[i][2]
            color = rgb_to_float(colors[cluster_id])
            colored_points.append([x, y, z, color])

    return colored_points


def get_cloud_clusters(clusters, cloud):

    # Get a random unique colors for each object
    number_of_clusters = len(clusters)

    colored_points = []

    # Assign a color for each point
    # Points with the same color belong to the same cluster
    for cluster_id, cluster in enumerate(clusters):
        for c, i in enumerate(cluster):
            x, y, z = cloud[i][0], cloud[i][1], cloud[i][2]
            colored_points.append([x, y, z])

    return colored_points


def random_color_gen():
    """ Generates a random color

        Args: None

        Returns:
            list: 3 elements, R, G, and B
    """
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return [r, g, b]


def get_color_list(cluster_count):
    """ Returns a list of randomized colors

        Args:
            cluster_count (int): Number of random colors to generate

        Returns:
            (list): List containing 3-element color lists
    """
    color_list = []
    if (cluster_count > len(color_list)):
        for i in range(len(color_list), cluster_count):
            color_list.append(random_color_gen())
    return color_list


def rgb_to_float(color):
    """ Converts an RGB list to the packed float format used by PCL

        From the PCL docs:
        "Due to historical reasons (PCL was first developed as a ROS package),
         the RGB information is packed into an integer and casted to a float"

        Args:
            color (list): 3-element list of integers [0-255,0-255,0-255]

        Returns:
            float_rgb: RGB value packed as a float
    """
    hex_r = (0xff & color[0]) << 16
    hex_g = (0xff & color[1]) << 8
    hex_b = (0xff & color[2])

    hex_rgb = hex_r | hex_g | hex_b

    float_rgb = struct.unpack('f', struct.pack('i', hex_rgb))[0]

    return float_rgb


def float_to_rgb(float_rgb):
    """ Converts a packed float RGB format to an RGB list

        Args:
            float_rgb: RGB value packed as a float

        Returns:
            color (list): 3-element list of integers [0-255,0-255,0-255]
    """
    s = struct.pack('>f', float_rgb)
    i = struct.unpack('>l', s)[0]
    pack = ctypes.c_uint32(i).value

    r = (pack & 0x00FF0000) >> 16
    g = (pack & 0x0000FF00) >> 8
    b = (pack & 0x000000FF)

    color = [r, g, b]

    return color
