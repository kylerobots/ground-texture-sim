"""!
This module provides the functions necessary to read in all the user's configurations and import the
provided trajectory data.
"""
import argparse
import json
from typing import Dict, List, Tuple
import numpy


def create_camera_pose(camera_configs: Dict) -> numpy.ndarray:
    """!
    @brief Determine the 4x4 homogenous matrix for the camera's pose relative to the "robot".

    This takes the camera position values from the config dictionary and creates a 4x4 homogenous
    transform matrix. This assumes RPY applied as intrinsic rotations.
    @param camera_configs The ['camera'] portion of the configuration JSON.
    @return A 4x4 Numpy array representing the pose of the camera in the robot's frame of reference.
    """
    pose = numpy.identity(4)
    pose[0, 3] = camera_configs['x']
    pose[1, 3] = camera_configs['y']
    pose[2, 3] = camera_configs['z']
    roll = camera_configs['roll']
    pitch = camera_configs['pitch']
    yaw = camera_configs['yaw']
    rotation_roll = numpy.array([
        [1.0, 0.0, 0.0],
        [0.0, numpy.cos(roll), -numpy.sin(roll)],
        [0.0, numpy.sin(roll), numpy.cos(roll)]
    ])
    rotation_pitch = numpy.array([
        [numpy.cos(pitch), 0.0, numpy.sin(pitch)],
        [0.0, 1.0, 0.0],
        [-numpy.sin(pitch), 0.0, numpy.cos(pitch)]
    ])
    rotation_yaw = numpy.array([
        [numpy.cos(yaw), -numpy.sin(yaw), 0.0],
        [numpy.sin(yaw), numpy.cos(yaw), 0.0],
        [0.0, 0.0, 1.0]
    ])
    pose[0:3, 0:3] = rotation_roll @ rotation_pitch @ rotation_yaw
    return pose


def load_configuration(args_list: List[str]) -> Tuple[Dict, List[List[float]]]:  # pragma: no cover
    """!
    @brief Parse the command line and read configuration information provided by the arguments.

    This function calls @ref _parse_args to determine which configuration file to load,
    @ref _load_config to actually read it in and verify correctness, and @ref _load_trajectory to
    read in the list of poses. If any fail, it throws an error.

    @param args_list The arguments straight from the command line.
    @return A tuple containing a well-formatted Dict of settings and a list of trajectories, where
    each item in the list is a list of the form [x, y, theta].
    @exception FileNotFoundError Raised if the config or trajectory files do not exist
    @exception JSONDecoderError Raised if the file is not in JSON format.
    @exception KeyError Raised if the required entries are not present in the JSON.
    @exception RuntimeError Raised if the pose format does not follow the correct structure.
    """
    config_file = _parse_args(args_list=args_list)
    config_dict = _load_config(config_file)
    trajectory_list = _load_trajectory(config_dict['trajectory'])
    return config_dict, trajectory_list


def _load_config(filename: str) -> Dict:
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
    @exception TypeError Raised if any values are the incorrect types.
    """
    with open(file=filename, mode='r', encoding='utf8') as file:
        configs = json.load(fp=file)
    # Check for required top level options
    required_keys = ['output', 'trajectory', 'camera', 'sequence']
    if not all(key in configs for key in required_keys):
        raise KeyError('Required value missing from JSON')
    # Verify the required camera values are present.
    required_camera_keys = ['name']
    if not all(key in configs['camera'] for key in required_camera_keys):
        raise KeyError('Camera name missing from camera_properties in JSON')
    # Fill in any optional camera values
    default_camera_properties = {
        'x': 0.0,
        'y': 0.0,
        'z': 0.0,
        'roll': 0.0,
        'pitch': 1.5708,
        'yaw': 0.0
    }
    for key, _ in default_camera_properties.items():
        if key not in configs['camera'].keys():
            configs['camera'][key] = default_camera_properties[key]
    # Verify the required sequence values are present
    required_sequence_keys = ['texture_number',
                              'sequence_type', 'sequence_number']
    if not all(key in configs['sequence'] for key in required_sequence_keys):
        raise KeyError('Required sequence information is missing')
    # Convert the texture number and sequence number to ints if not already
    try:
        configs['sequence']['sequence_number'] = int(
            configs['sequence']['sequence_number'])
    except (TypeError, ValueError) as ex:
        raise TypeError('sequence_number must be an integer') from ex
    try:
        configs['sequence']['texture_number'] = int(
            configs['sequence']['texture_number'])
    except (TypeError, ValueError) as ex:
        raise TypeError('texture_number must be an integer') from ex
    return configs


def _load_trajectory(filename: str) -> List[List[float]]:
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
                    F'Each pose must be 3 floats, separated by commas. Got: {line}')
            try:
                single_pose = []
                for element in pose_strings:
                    single_pose.append(float(element))
                result.append(single_pose)
            except Exception as error:
                raise RuntimeError(
                    F'Each pose must be 3 floats, separated by commas. Got: {line}') from error
    return result


def _parse_args(args_list: List[str]) -> str:
    """!
    @brief Parse the command line for the location of the configuration file.

    Since this is only ever called as part of Blender, it must first remove any Blender-specific
    arguments. Blender ignores everything after a '--', so use that to split. Then, the only
    required argument is the JSON file location.

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
