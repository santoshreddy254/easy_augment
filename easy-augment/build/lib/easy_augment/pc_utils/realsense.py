# License: Apache 2.0. See LICENSE file in root directory.
# Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################
import pyrealsense2 as rs
import numpy as np
import cv2
import pcl
from easy_augment.pc_utils.helper import *


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)


# Get stream profile and camera intrinsics
profile = pipeline.get_active_profile()
depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
depth_intrinsics = depth_profile.get_intrinsics()
w, h = depth_intrinsics.width, depth_intrinsics.height
try:
    count = 0
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 3)
        depth_frame = spatial.process(depth_frame)
        if count > 10:
            # depth_frame = frames.get_depth_frame()
            # color_frame = frames.get_color_frame()
            pc = rs.pointcloud()
            pc.map_to(color_frame)
            pointcloud = pc.calculate(depth_frame)
            v = pointcloud.get_vertices()
            verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)
            cloud0 = pcl.PointCloud(verts)
            filtered_cloud = do_passthrough_filter(point_cloud=cloud0,
                                                   name_axis='z', min_axis=0.0, max_axis=0.6)
            downsampled_cloud = do_voxel_grid_filter(point_cloud=filtered_cloud, LEAF_SIZE=0.01)

            table_cloud, objects_cloud = do_ransac_plane_segmentation(
                downsampled_cloud, max_distance=0.01)
            project_inliers = objects_cloud.make_ProjectInliers()
            project_inliers.set_model_type(pcl.SACMODEL_NORMAL_PARALLEL_PLANE)
            plane = project_inliers.filter()
            colorless_cloud = XYZRGB_to_XYZ(plane)
            print(colorless_cloud.size)
            clusters = get_clusters(colorless_cloud, tolerance=0.02, min_size=100, max_size=25000)

            colored_points = get_colored_clusters(clusters, colorless_cloud)

      # Create a cloud with each cluster of points having the same color
            clusters_cloud = pcl.PointCloud_PointXYZRGB()
            clusters_cloud.from_list(colored_points)
            pcl.save(downsampled_cloud, "12.ply")
            print(clusters_cloud.size)
            if clusters_cloud.size > 0:
                pcl.save(clusters_cloud, "13.ply")
        if not depth_frame or not color_frame:
            continue
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
            depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Stack both images horizontally
        images = np.hstack((color_image, depth_colormap))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)
        count += 1
        # break

finally:

    # Stop streaming
    pipeline.stop()
