"""!
This module provides the script to interact with Blender for image and pose
generation.

It reads in desired settings from a user-specified JSON, then moves
the camera around in Blender to collect data. Lastly, data is output to the
specified directory.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import argparse
import json
import sys
from typing import Dict, List


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
        parameters = json.load(fp=file)
    # Check for required options
    if 'trajectory' not in parameters.keys() or 'output' not in parameters.keys():
        raise KeyError('Required values "output" and "trajectory" not in JSON')
    return parameters


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

    print('##########')
    for temp_arg in args_list:
        print(temp_arg)
    print('##########')
    parser = argparse.ArgumentParser(
        description='A script to generate texture data in Blender.')
    parser.add_argument(
        'parameter_file', help='The JSON file specifying all parameters.')
    parsed_args = parser.parse_args(args_list)
    param_file = parsed_args.parameter_file
    return param_file


if __name__ == '__main__':  # pragma: no cover
    parameter_file = parse_args(sys.argv)
