"""!
This module provides the script to interact with Blender for image and pose
generation.

It reads in desired settings from a user-specified JSON, then moves
the camera around in Blender to collect data. Lastly, data is output to the
specified directory.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import sys
import data_generation


def main() -> None:  # pragma: no cover
    """!
    Run through the program script.

    First, find the JSON. Then, load it and the trajectory specified by it.
    Last, interact with Blender to create the data.

    @return None
    """
    config_dict, trajectory_list = data_generation.configuration_loader.load_configuration(
        sys.argv)
    data_generation.blender_interface.generate_images(
        config_dict, trajectory_list)
    data_generation.data_output.write_camera_intrinsic_matrix(
        config_dict['camera_properties']['name'], config_dict['output'])
    data_generation.data_output.write_camera_pose(
        config_dict['camera_properties'], config_dict['output'])
    data_generation.data_output.write_trajectory(config_dict['output'] +
                                                 '/trajectory.txt', trajectory_list)


if __name__ == '__main__':  # pragma: no cover
    main()
