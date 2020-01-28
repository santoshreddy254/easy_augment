import pyrealsense2 as rs
import numpy as np
import cv2
import pcl
from easy_augment.pc_utils.helper import *
import imutils


def init_capture_data():
    """Short summary.

    Returns
    -------
    type
        Description of returned object.

    """
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    return pipeline, config


def get_object_points(color_frame, depth_frame):
    """Short summary.

    Parameters
    ----------
    color_frame : type
        Description of parameter `color_frame`.
    depth_frame : type
        Description of parameter `depth_frame`.

    Returns
    -------
    type
        Description of returned object.

    """
    pc = rs.pointcloud()
    pc.map_to(color_frame)
    pointcloud = pc.calculate(depth_frame)
    v = pointcloud.get_vertices()
    verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)
    cloud = pcl.PointCloud(verts)
    filtered_cloud = do_passthrough_filter(point_cloud=cloud,
                                           name_axis='z', min_axis=0.0, max_axis=0.6)
    downsampled_cloud = do_voxel_grid_filter(point_cloud=filtered_cloud, LEAF_SIZE=0.004)

    table_cloud, objects_cloud = do_ransac_plane_segmentation(
        downsampled_cloud, max_distance=0.01)
    # project_inliers = objects_cloud.make_ProjectInliers()
    # project_inliers.set_model_type(pcl.SACMODEL_NORMAL_PARALLEL_PLANE)
    # plane = project_inliers.filter()
    colorless_cloud = XYZRGB_to_XYZ(objects_cloud)
    clusters = get_clusters(objects_cloud, tolerance=0.02, min_size=100, max_size=25000)

    colored_points = get_cloud_clusters(clusters, colorless_cloud)
    # Create a cloud with each cluster of points having the same color
    clusters_cloud = pcl.PointCloud()
    clusters_cloud.from_list(colored_points)
    color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
    depth_to_color_extrin = depth_frame.profile.get_extrinsics_to(color_frame.profile)
    Pixel_Coord = []
    for data in clusters_cloud:
        if np.round(data[2], 2) > 0.1:
            color_point = rs.rs2_transform_point_to_point(depth_to_color_extrin, list(data))
            Pixel_Coord.append(rs.rs2_project_point_to_pixel(color_intrin, color_point))
    # pcl.save(downsampled_cloud, "12.ply")
    # if clusters_cloud.size > 0:
    #     pcl.save(clusters_cloud, "13.ply")
    return Pixel_Coord


def get_mask(Pixel_Coord, color_frame):
    """Short summary.

    Parameters
    ----------
    Pixel_Coord : type
        Description of parameter `Pixel_Coord`.

    Returns
    -------
    type
        Description of returned object.

    """
    cluster_img = np.zeros((480, 640, 3), np.uint8)
    thresh = np.zeros((480, 640), 'uint8')
    x_sum = y_sum = 0
    for px in Pixel_Coord:
        thresh[int(px[1]), int(px[0])] = 255
    kernel = np.ones((3, 3), np.uint8)
    im_opening = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(im_opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts = np.concatenate(contours)
    hull = [cv2.convexHull(conts, True)]
    Pixel_Coord = np.asarray(Pixel_Coord)
    x_min = np.min(Pixel_Coord[:, 0])
    x_max = np.max(Pixel_Coord[:, 0])

    y_min = np.min(Pixel_Coord[:, 1])
    y_max = np.max(Pixel_Coord[:, 1])

    # color_frame_crop = color_frame[int(x_min)-10:int(x_max)+10, int(y_min)-10:int(y_max)+10]
    # # cv2.imshow("croped", color_frame_crop)
    # gray = cv2.cvtColor(color_frame_crop, cv2.COLOR_BGR2GRAY)
    # bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                            cv2.THRESH_BINARY, 11, 2)
    # # edged = cv2.Canny(bw, th/2, th)
    # edged = cv2.Canny(bw, 30, 200)
    # cnts, h = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # # cnts = imutils.grab_contours(cnts)
    # cnts = np.concatenate(cnts)
    # hull2 = [cv2.convexHull(cnts, True)]
    # hull2 = np.asarray(hull2)
    # hull2[0][:, 0][:, 0] += int(x_min)
    # hull2[0][:, 0][:, 1] += int(y_min)
    # hull2 = list(hull2)
    # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    color_frame = cv2.rectangle(color_frame, (int(x_min)-10, int(y_min)-10),
                                (int(x_max)+10, int(y_max)+10), (0, 255, 0), 2)
    cv2.drawContours(cluster_img, hull, -1, (255, 255, 255), -1, 8)
    # cv2.drawContours(color_frame, hull2, -1, (0, 255, 255), 2, 8)
    cv2.drawContours(color_frame, hull, -1, (0, 255, 0), 2, 8)
    # cv2.waitKey(1)
    # cv2.destroyAllWindows()
    return color_frame, cluster_img
