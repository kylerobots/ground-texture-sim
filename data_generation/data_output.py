"""!
This module provides the functions necessary to write data to file.
"""
import os
from math import cos, sin
from typing import Dict, List
from data_generation import blender_interface


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
    """
    matrix_string = blender_interface.get_camera_intrinsic_matrix(
        camera_name=camera_name)
    # Make sure the subdirectory exists before writing.
    subfolder = os.path.join(output_folder, 'camera_properties')
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    filename = os.path.join(subfolder, F'{camera_name}_intrinsic_matrix.txt')
    with open(file=filename, mode='w', encoding='utf8') as file:
        for i in [0, 3, 6]:
            file.write(
                F'{matrix_string[i]} {matrix_string[i+1]} {matrix_string[i+2]}\n')


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
    matrix_string = F'{a11:.6f}, {a12:.6f}, {a13:.6f}, {x_pos:.6f}\n' \
        F'{a21:.6f}, {a22:.6f}, {a23:.6f}, {y_pos:.6f}\n' \
        F'{a31:.6f}, {a32:.6f}, {a33:.6f}, {z_pos:.6f}\n' \
        '0.000000, 0.000000, 0.000000, 1.000000\n'
    # Make sure the subdirectory exists before writing.
    subfolder = os.path.join(output_folder, 'camera_properties')
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    filename = os.path.join(subfolder, F'{camera_properties["name"]}_pose.txt')
    with open(file=filename, mode='w', encoding='utf8') as output:
        output.write(matrix_string)


def write_trajectory(filename: str, trajectory: List[List[float]]) -> None:
    """!
    Write the poses in the trajectory to a file.

    This creates a single file with one line per pose. The line is of the form "x, y, theta".

    @param filename The location to write to.
    @param trajectory The list of poses to write, in [x, y, theta] format.
    @return None
    @exception RuntimeError Raised if the pose format does not follow the correct structure.
    """
    # Create the string to write and verify the format along the way.
    trajectory_string = ''
    try:
        for pose in trajectory:
            trajectory_string += F'{pose[0]:f}, {pose[1]:f}, {pose[2]:f}\n'
    except Exception as ex:
        raise RuntimeError(
            F'Pose must be [x, y, theta] format, not {pose}.') from ex
    with open(file=filename, mode='w', encoding='utf8') as output:
        output.write(trajectory_string)
