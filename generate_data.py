"""!
This module provides the script to interact with Blender for image and pose
generation.

It reads in desired settings from a user-specified JSON, then moves
the camera around in Blender to collect data. Lastly, data is output to the
specified directory.

SPDX-License-Identifier: GPL-3.0-or-later
"""
from typing import List
import argparse
import sys
import data_generation


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
    config_dict = data_generation.configuration_setup.load_config(config_file)
    trajectory_list = data_generation.configuration_setup.load_trajectory(
        config_dict['trajectory'])
    data_generation.blender_interface.generate_images(
        config_dict, trajectory_list)
    data_generation.data_output.write_camera_calibration(
        config_dict['output'] + '/camera_calibration.txt')
    data_generation.data_output.write_camera_pose(config_dict['output'] + '/camera_pose.txt',
                                                  config_dict['camera_properties'])
    data_generation.data_output.write_trajectory(config_dict['output'] +
                                                 '/trajectory.txt', trajectory_list)


if __name__ == '__main__':  # pragma: no cover
    main()
