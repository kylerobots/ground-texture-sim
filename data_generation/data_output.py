"""!
This module provides the functions necessary to write data to file.
"""
from math import cos, sin
from typing import Dict, List
import bpy


def write_camera_calibration(filename: str) -> None:
    """!
    Create a file with the camera's intrinsic matrix.

    This is a 3x3 matrix, with one row of the matrix per line. Each element is separated by a comma.
    The formula for deriving the matrix is from
    https://visp-doc.inria.fr/doxygen/visp-3.4.0/tutorial-tracking-mb-generic-rgbd-Blender.html

    @param filename The location to store the file.
    @return None
    """
    camera = bpy.data.objects['Camera']
    focal_length = camera.data.lens
    scene = bpy.context.scene
    resolution_x_px = scene.render.resolution_x
    resolution_y_px = scene.render.resolution_y
    scale = scene.render.resolution_percentage / 100.0
    sensor_width_mm = camera.data.sensor_width
    sensor_height_mm = camera.data.sensor_height
    aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
    if camera.data.sensor_fit == 'VERTICAL':
        s_u = resolution_x_px * scale / sensor_width_mm / aspect_ratio
        s_v = resolution_y_px * scale / sensor_height_mm
    else:
        aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
        s_u = resolution_x_px * scale / sensor_width_mm
        s_v = resolution_y_px * scale * aspect_ratio / sensor_height_mm
    alpha_u = focal_length * s_u
    alpha_v = focal_length * s_v
    u_0 = resolution_x_px * scale / 2
    v_0 = resolution_y_px * scale / 2
    skew = 0
    with open(file=filename, mode='w', encoding='utf8') as file:
        file.write(F'{alpha_u}, {skew}, {u_0}\n')
        file.write(F'0.0, {alpha_v}, {v_0}\n')
        file.write('0.0, 0.0, 1.0\n')


def write_camera_pose(filename: str, camera_properties: Dict) -> None:
    """!
    Create a file containing the homogenous transform matrix of the transform
    between the robot origin and camera origin.

    This will be a text file with 4 lines with 4 numbers per line, separated by
    a comma and a space. The elements of this file correspond to the 4x4
    homogenous transform matrix that shows the pose of the camera as measured
    from the robot's/trajectory's frame of reference.

    @param filename The location to write to.
    @param camera_properties A formatted dictionary with all 6 pose elements, as provided by
    @ref configuration_loader::load_configuration
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
