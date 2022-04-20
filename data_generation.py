"""!
This module provides the script to interact with Blender for image and pose
generation.

It reads in desired settings from a user-specified JSON, then moves
the camera around in Blender to collect data. Lastly, data is output to the
specified directory.

SPDX-License-Identifier: GPL-3.0-or-later
"""
from math import cos, pi, sin
from typing import Dict, List
import argparse
import json
import sys
import bpy
import mathutils


def generate_images(configs: Dict, trajectory: List[List[float]]) -> None:
    """!
    Generate an image at each trajectory point via Blender's interface.

    This iterates through each pose in the trajectory, moves the camera to the correct spot, then
    renders the image.

    @param configs The configuration values specified in the JSON file.
    @param trajectory A list of poses, of the form [x, y, theta].
    @return None
    """
    camera = bpy.data.objects['Camera']
    # Calculate the trajectory to camera transform from the provided parameters.
    trajectory_2_camera_translation = mathutils.Matrix.Translation(
        (configs['camera_properties']['x'], configs['camera_properties']['y'],
         configs['camera_properties']['z']))
    trajectory_2_camera_rotation = mathutils.Euler((configs['camera_properties']['roll'],
                                                    configs['camera_properties']['pitch'],
                                                    configs['camera_properties']['yaw']),
                                                   'XYZ').to_matrix().to_4x4()
    trajectory_2_camera = trajectory_2_camera_translation @ trajectory_2_camera_rotation
    # Blender's origin pose is pointing straight down. While this may seem beneficial, it is
    # inconsistent with robot frame conventions, so apply a correcting factor that, if
    # trajectory_2_camera is identity, aligns the camera with the trajectory/robot pose.
    blender_adjustment = mathutils.Euler(
        (pi/2.0, 0.0, -pi/2.0), 'XYZ').to_matrix().to_4x4()
    trajectory_2_camera = trajectory_2_camera @ blender_adjustment
    # Iterate through each pose in the trajectory
    for i, pose in enumerate(trajectory):
        # Figure out the camera's global pose by combining this pose with the one computed above.
        trajectory_pose_rotation = mathutils.Matrix.Rotation(pose[2], 4, 'Z')
        trajectory_pose_translation = mathutils.Matrix.Translation(
            (pose[0], pose[1], 0.0))
        trajectory_pose = trajectory_pose_translation @ trajectory_pose_rotation
        # Combine them to get the camera's pose
        camera_pose = trajectory_pose @ trajectory_2_camera
        # Use this to position in Blender
        camera.location.x = camera_pose.to_translation()[0]
        camera.location.y = camera_pose.to_translation()[1]
        camera.location.z = camera_pose.to_translation()[2]
        camera.rotation_euler.x = camera_pose.to_euler('XYZ')[0]
        camera.rotation_euler.y = camera_pose.to_euler('XYZ')[1]
        camera.rotation_euler.z = camera_pose.to_euler('XYZ')[2]
        # Render the image into the output directory
        bpy.context.scene.render.filepath = F'{configs["output"]}/{i:06d}.png'
        bpy.ops.render.render(write_still=True)


def load_config(filename: str) -> Dict:
    """!
    Read in the user provided configuration JSON.

    This also checks that all required elements are present. An Exception is raised if not. If an
    optional element is not present, a default value is assumed.

    @param filename The JSON file to read. May be absolute or relative path.
    @return A well-formed dictionary of configuration options. This is guaranteed to have every
    element referenced by the script.
    @exception FileNotFoundError Raised if the file provided in filename does
    not exist.
    @exception KeyError Raised if the required entries are not present in the
    JSON.
    @exception JSONDecoderError Raised if the file is not in JSON format.
    """
    with open(file=filename, mode='r', encoding='utf8') as file:
        configs = json.load(fp=file)
    # Check for required options
    required_keys = ['output', 'trajectory']
    if not all(key in configs for key in required_keys):
        raise KeyError('Required value missing from JSON')
    # Fill in default values, if not provided.
    default_camera_properties = {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
        'roll': 0.0,
        'pitch': pi / 2.0,
        'yaw': 0.0
    }
    if 'camera_properties' not in configs.keys():
        configs['camera_properties'] = default_camera_properties
    for key, _ in default_camera_properties.items():
        if key not in configs['camera_properties'].keys():
            configs['camera_properties'][key] = default_camera_properties[key]
    return configs


def load_trajectory(filename: str) -> List[List[float]]:
    """!
    Read in the poses from the trajectory file.

    The file should be structured with one pose per line. The poses are stored as X, Y, Theta
    (whitespace is optional). The theta value should be in radians. These coordinates are where the
    "robot" will be placed in the simulated world.

    @param filename The file to read from. May be absolute or relative path.
    @return A list of poses, where each item in the list is a list of the form [x, y, theta].
    @exception FileNotFoundError Raised if the file provided in filename does not exist.
    @exception RuntimeError Raised if the pose format does not follow the correct structure.
    """
    result = []
    with open(file=filename, mode='r', encoding='utf8') as file:
        for line in file:
            # Strip off any whitespace and newlines
            line = line.strip(' \n\r\t')
            # If the line is empty at this point, it is just a blank line and
            # can be skipped
            if len(line) == 0:
                continue
            pose_strings = line.split(sep=',')
            if len(pose_strings) != 3:
                raise RuntimeError(
                    F'Each pose must be 3 floats, seperated by commas. Got: {line}')
            try:
                single_pose = []
                for element in pose_strings:
                    single_pose.append(float(element))
                result.append(single_pose)
            except Exception as error:
                raise RuntimeError(
                    F'Each pose must be 3 floats, seperated by commas. Got: {line}') from error
    return result


def parse_args(args_list: List[str]) -> str:
    """!
    Parse the command line specifications.

    Since this is only ever called as part of Blender, it must first remove any
    Blender-specific arguments. Blender ignores everything after a '--', so use
    that to split. Then, the only required argument is the JSON file location.

    @param args_list The arguments straight from the command line
    @return The filename of the JSON.
    """
    if '--' not in args_list:
        args_list = []
    else:
        args_list = args_list[args_list.index('--') + 1:]
    parser = argparse.ArgumentParser(
        description='A script to generate texture data in Blender.')
    parser.add_argument(
        'parameter_file', help='The JSON file specifying all parameters.')
    parsed_args = parser.parse_args(args_list)
    param_file = parsed_args.parameter_file
    return param_file


def write_camera_calibration(filename: str) -> None:
    """!
    Create a file with the camera's intrinsic matrix.

    This is a 3x3 matrix, with one row of the matrix per line. Each element is seperated by a comma.
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

    This will be a text file with 4 lines with 4 numbers per line, seperated by
    a comma and a space. The elements of this file correspond to the 4x4
    homogenous transform matrix that shows the pose of the camera as measured
    from the robot's/trajectory's frame of reference.

    @param filename The location to write to.
    @param camera_properties A formatted dictionary with all 6 pose elements, as provided by
    @ref load_config
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


def main() -> None:  # pragma: no cover
    """!
    Run through the program script.

    First, find the JSON. Then, load it and the trajectory specified by it.
    Last, interact with Blender to create the data.

    @return None
    """
    config_file = parse_args(sys.argv)
    config_dict = load_config(config_file)
    trajectory_list = load_trajectory(config_dict['trajectory'])
    generate_images(config_dict, trajectory_list)
    write_camera_calibration(config_dict['output'] + '/camera_calibration.txt')
    write_camera_pose(config_dict['output'] +
                      '/camera_pose.txt', config_dict['camera_properties'])
    write_trajectory(config_dict['output'] +
                     '/trajectory.txt', trajectory_list)


if __name__ == '__main__':  # pragma: no cover
    main()
