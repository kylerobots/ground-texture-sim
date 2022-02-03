"""!
This module provides the script to interact with Blender for image and pose
generation.

It reads in desired settings from a user-specified JSON, then moves
the camera around in Blender to collect data. Lastly, data is output to the
specified directory.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import argparse
from math import pi
import json
import sys
from typing import Dict, List
import bpy


def generate_data(configs: Dict, trajectory: List[List[float]]) -> None:
    """!
    Interact with Blender to make the images.

    @param configs The configuration values specified in the JSON file.
    @param trajectory A list of poses, of the form [x, y, theta].
    @return None
    """
    camera = bpy.data.objects['Camera']
    # Set the camera angle and height, since those don't change.
    camera.location.z = configs['camera height']
    camera.rotation_euler.x = 0.0
    camera.rotation_euler.y = 0.0
    for i, pose in enumerate(trajectory):
        camera.location.x = pose[0]
        camera.location.y = pose[1]
        # Offset the pose by -pi/2, since at 0, the top of the image is towards
        # positive y.
        camera.rotation_euler.z = pose[2] - pi/2.0
        bpy.context.scene.render.filepath = F'{configs["output"]}/{i:06d}.png'
        bpy.ops.render.render(write_still=True)
    # Lastly, write the camera parameters to file. See
    # https://visp-doc.inria.fr/doxygen/visp-3.4.0/tutorial-tracking-mb-generic-rgbd-Blender.html
    # for details.
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
    with open(file=F'{configs["output"]}/calibration.txt', mode='w', encoding='utf8') as file:
        file.write(F'{alpha_u}, {skew}, {u_0}\n')
        file.write(F'0.0, {alpha_v}, {v_0}\n')
        file.write('0.0, 0.0, 1.0\n')


def read_config(filename: str) -> Dict:
    """!
    Reads in the configuration JSON and verifies required components.

    This reads the JSON file specified in filename. It also checks that, at a
    minimum, the output directory and trajectory file have been specified. If
    they are not, an Exception is raised.

    @param filename The JSON file to read. May be absolute or relative path.
    @return The JSON, loaded as a Dict.
    @exception FileNotFoundError Raised if the file provided in filename does
    not exist.
    @exception KeyError Raised if the required entries are not present in the
    JSON.
    @exception JSONDecoderError Raised if the file is not in JSON format.
    """
    with open(file=filename, mode='r', encoding='utf8') as file:
        configs = json.load(fp=file)
    # Check for required options
    required_keys = ['camera height', 'output', 'trajectory']
    if not all(key in configs for key in required_keys):
        raise KeyError('Required value missing from JSON')
    return configs


def read_poses(filename: str) -> List[List[float]]:
    """!
    Read poses from a provided file.

    The file should be structured with one pose per line. The poses are stored
    as X, Y, Theta (whitespace is optional). The theta value should be in
    radians. These coordinates are where the camera will be placed in the
    simulated world.

    @param filename The file to read from. May be absolute or relative path.
    @return A list of poses, where each item in the list is a list of the form
    [x, y, theta].
    @exception FileNotFoundError Raised if the file provided in filename does
    not exist.
    @exception RuntimeError Raised if the pose format does not follow the
    correct structure.
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


def main() -> None:  # pragma: no cover
    """!
    Run through the program script.

    First, find the JSON. Then, load it and the trajectory specified by it.
    Last, interact with Blender to create the data.

    @return None
    """
    config_file = parse_args(sys.argv)
    config_dict = read_config(config_file)
    trajectory_list = read_poses(config_dict['trajectory'])
    generate_data(config_dict, trajectory_list)


if __name__ == '__main__':  # pragma: no cover
    main()
