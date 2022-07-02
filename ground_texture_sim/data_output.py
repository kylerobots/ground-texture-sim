"""!
This module provides the functions necessary to write data to file.
"""
import os
from math import cos, sin
from typing import Dict, List
import numpy
from ground_texture_sim import blender_interface, configuration_loader, name_configuration


def _project_image_corner(camera_matrix: numpy.ndarray, camera_pose: numpy.ndarray,
                          robot_pose: numpy.ndarray) -> numpy.ndarray:
    """!
    Take the top left corner of the camera image and project it into a global camera pixel frame.

    To do this, first project into the frame of the robot. Then, transform that to the origin. Then,
    project into an imaginary camera that is located as if its robot was at the origin.

    @param camera_matrix The 3x3 camera intrinsic matrix.
    @param camera_pose The 4x4 homogenous transform that represents the pose of the camera as
    measured from the robot frame.
    @param robot_pose The 4x4 homogenous transform that represents the pose of the robot as measured
    from the origin.
    @return A 2 element array that represents the point in a global camera frame.
    """
    # The top left corner is always the origin in the pixel coordinate system
    point_pixel = numpy.array([0.0, 0.0, 1.0])
    # Assume the camera height is the Z component of its pose.
    camera_height = camera_pose[2, 3]
    # Project into the image frame. This normally is only up to a scale factor, but we know the
    # height so can make that scale.
    point_image = numpy.linalg.inv(camera_matrix) @ point_pixel * camera_height
    point_image = numpy.append(point_image, numpy.array([1.0]))
    # The rotation into the camera frame is always the same
    image_2_camera_transform = numpy.array([
        [0.0, 0.0, 1.0, 0.0],
        [-1.0, 0.0, 0.0, 0.0],
        [0.0, -1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])
    # Transform into the global frame
    point_robot = camera_pose @ image_2_camera_transform @ point_image
    point_origin = robot_pose @ point_robot
    # Now project back into an imaginary camera as if the robot was at the origin.
    point_fake_image = numpy.linalg.inv(
        image_2_camera_transform) @ numpy.linalg.inv(camera_pose) @ point_origin
    # Use the height and camera matrix to project into pixels. Drop the Z, since it will be
    # normalized out
    point_fake_image = numpy.delete(point_fake_image, 3)
    point_fake_pixels = camera_matrix @ (point_fake_image / camera_height)
    # We only need the x and y values.
    return point_fake_pixels[0:2].flatten()


def prepare_output_folder(output_folder: str) -> None:
    """!
    Creates the output folder and subfolders if they don't exist already.

    This ensures output_folder exists and the subfolder `camera_properties` exists as well.

    @param output_folder The folder to create.
    @return None
    """
    subfolder_camera = os.path.join(output_folder, 'camera_properties')
    if not os.path.exists(subfolder_camera):
        os.makedirs(subfolder_camera)


def write_camera_intrinsic_matrix(camera_name: str, output_folder: str) -> None:
    """!
    Create a file with the camera's intrinsic matrix.

    This is a 3x3 matrix, with one row of the matrix per line. Each element is separated by a space.
    The name of the file will be `name_intrinsic_matrix.txt` where `name` is the value in
    camera_name. This file is located in a subdirectory of the specified output folder called
    `camera_properties`.

    @param camera_name The name of the camera in Blender.
    @param output_folder The location to store the file.
    @return None
    @exception NameError thrown if the camera name doesn't exist in the simulation.
    """
    try:
        matrix_string = blender_interface.get_camera_intrinsic_matrix(
            camera_name=camera_name)
    except Exception as exc:
        raise NameError(
            F'Unable to get camera properties for {camera_name}') from exc
    filename = os.path.join(
        output_folder, 'camera_properties', F'{camera_name}_intrinsic_matrix.txt')
    with open(file=filename, mode='w', encoding='utf8') as file:
        output_string = ''
        for i in [0, 3, 6]:
            output_string += (
                F'{matrix_string[i]:.6f} '
                F'{matrix_string[i+1]:.6f} '
                F'{matrix_string[i+2]:.6f}\n'
            )
        file.write(output_string)


def write_camera_pose(camera_properties: Dict, output_folder: str) -> None:
    """!
    Create a file containing the homogenous transform matrix of the transform between the robot
    origin and camera origin.

    This will be a text file with 4 lines with 4 numbers per line, separated by a space. The
    elements of this file correspond to the 4x4 homogenous transform matrix that shows the pose of
    the camera as measured from the robot's/trajectory's frame of reference.

    The file will be called `name_pose.txt` where `name` is the name of the camera in Blender as
    specified by the `camera_properties.name` entry in the configuration JSON. This file is placed
    in a subfolder of output_folder called `camera_properties`.

    @param camera_properties A formatted dictionary with all 6 pose elements, as provided by
    @ref configuration_loader::load_configuration
    @param output_folder The folder to create the subfolder in.
    @return None
    """
    x_pos = camera_properties['x']
    y_pos = camera_properties['y']
    z_pos = camera_properties['z']
    roll = camera_properties['roll']
    pitch = camera_properties['pitch']
    yaw = camera_properties['yaw']
    a11 = cos(pitch)*cos(yaw)
    a12 = -cos(roll)*sin(yaw) + sin(roll)*sin(pitch)*cos(yaw)
    a13 = sin(roll)*sin(yaw) + cos(roll)*sin(pitch)*cos(yaw)
    a21 = cos(pitch)*sin(yaw)
    a22 = cos(roll)*cos(yaw) + sin(roll)*sin(pitch)*sin(yaw)
    a23 = -sin(roll)*cos(yaw) + cos(roll)*sin(pitch)*sin(yaw)
    a31 = -sin(pitch)
    a32 = sin(roll)*cos(pitch)
    a33 = cos(roll)*cos(pitch)
    matrix_string = F'{a11:.6f} {a12:.6f} {a13:.6f} {x_pos:.6f}\n' \
        F'{a21:.6f} {a22:.6f} {a23:.6f} {y_pos:.6f}\n' \
        F'{a31:.6f} {a32:.6f} {a33:.6f} {z_pos:.6f}\n' \
        '0.000000 0.000000 0.000000 1.000000\n'
    filename = os.path.join(
        output_folder, 'camera_properties', F'{camera_properties["name"]}_pose.txt')
    with open(file=filename, mode='w', encoding='utf8') as output:
        output.write(matrix_string)


def write_list_files(configs: Dict, trajectory_list: List[List[float]]) -> None:
    """!
    Write the three files that serve as the records of poses and image files.

    All files have a similar name scheme of *sequence_type*_*date*. The differences are:
    1. One ends in a *.test* extension and lists only the image files, relative to the directory of
    this list file.
    2. One ends in a *.txt* extension and alternates between the image file name and the pixel
    coordinates pose of the top left corner of the image.
    3. One ends in a *_meters.txt* suffix and extension and alternates between the image file name
    and the real world coordinates of the robot when each image is taken.

    @param configs The Dict of settings, used to create the file names and contents.
    @param trajectory_list The list of x, y, theta, trajectories as read from file.
    @return None
    """
    base_name = name_configuration.create_file_list_base(configs)
    # These files will be located at the output folder
    base_name_and_path = os.path.join(configs["output"], base_name)
    # Assemble the list of images first, since they are used in each file.
    image_path_list = []
    for i in range(len(trajectory_list)):
        image_path_abs = name_configuration.create_image_path(i, configs)
        # Since the above path is absolute, get its relative location from the output folder
        image_path_rel = os.path.relpath(image_path_abs, configs['output'])
        image_path_rel += '\n'
        image_path_list.append(image_path_rel)
    # Write the image paths
    with open(file=F'{base_name_and_path}.test', mode='w', encoding='utf-8') as test_file:
        for image_path in image_path_list:
            test_file.write(image_path)
    # Now write the image paths with the ground truths to the _meters file.
    with open(file=F'{base_name_and_path}_meters.txt', mode='w',
              encoding='utf-8') as ground_truth_file:
        for i, trajectory in enumerate(trajectory_list):
            ground_truth_file.write(image_path_list[i])
            pose_x = trajectory[0]
            pose_y = trajectory[1]
            pose_t = trajectory[2]
            ground_truth_string = F'{cos(pose_t):0.6f} {-sin(pose_t):0.6f} {pose_x:0.6f} ' \
                F'{sin(pose_t):0.6f} {cos(pose_t):0.6f} {pose_y:0.6f} ' \
                F'{0:0.6f} {0:0.6f} {1:0.6f}\n'
            ground_truth_file.write(ground_truth_string)
    # Now write the image paths with the pixel corners.
    # This requires the camera matrix and camera pose transform.
    camera_matrix = numpy.array(blender_interface.get_camera_intrinsic_matrix(
        configs['camera']['name'])).reshape((3, 3))
    camera_pose = configuration_loader.create_camera_pose(configs['camera'])
    with open(file=F'{base_name_and_path}.txt', mode='w', encoding='utf-8') as ground_truth_file:
        for i, trajectory in enumerate(trajectory_list):
            ground_truth_file.write(image_path_list[i])
            # Create the robot pose and use to project the top-left pixel into a global frame
            pose_x = trajectory[0]
            pose_y = trajectory[1]
            pose_t = trajectory[2]
            robot_pose = numpy.array([
                [cos(pose_t), -sin(pose_t), 0.0, pose_x],
                [sin(pose_t), cos(pose_t), 0.0, pose_y],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0]
            ])
            pixel_pose = _project_image_corner(
                camera_matrix, camera_pose, robot_pose)
            pixel_string = F'{cos(pose_t):0.6f} {-sin(pose_t):0.6f} {pixel_pose[0]:0.6f} ' \
                F'{sin(pose_t):0.6f} {cos(pose_t):0.6f} {pixel_pose[1]:0.6f} ' \
                F'{0:0.6f} {0:0.6f} {1:0.6f}\n'
            ground_truth_file.write(pixel_string)
