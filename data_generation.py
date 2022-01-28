"""!
This module provides the script to interact with Blender for image and pose
generation.

It reads in desired settings from a user-specified JSON, then moves
the camera around in Blender to collect data. Lastly, data is output to the
specified directory.

SPDX-License-Identifier: GPL-3.0-or-later
"""
from typing import List


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
    @raises RuntimeError Raised if the pose format does not follow the correct
    structure.
    @raises FileNotFoundError Raised if the file provided in filename does not
    exist.
    """
    result = []
    with open(file=filename, mode='r', encoding='utf8') as file:
        for line in file:
            # Strip off any whitespace and newlines
            line = line.strip(' \n\r\t')
            # If the line is empty at this point, it is just a blank line and can be skipped
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
