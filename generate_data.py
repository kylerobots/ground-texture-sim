"""!
This module provides the script to interact with Blender for image and pose
generation.

It reads in desired settings from a user-specified JSON, then moves
the camera around in Blender to collect data. Lastly, data is output to the
specified directory.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import sys
from ground_texture_sim.script_runner import GroundTextureSim


def main() -> None:  # pragma: no cover
    """!
    Run through the program script.

    First, find the JSON. Then, load it and the trajectory specified by it.
    Last, interact with Blender to create the data.

    @return None
    """
    simulator = GroundTextureSim(sys.argv)
    simulator.run()
    # config_dict, trajectory_list = ground_texture_sim.configuration_loader.load_configuration(
    #     sys.argv)
    # ground_texture_sim.blender_interface.generate_images(
    #     config_dict, trajectory_list)
    # ground_texture_sim.data_output.prepare_output_folder(config_dict['output'])
    # ground_texture_sim.data_output.write_camera_intrinsic_matrix(
    #     config_dict['camera']['name'], config_dict['output'])
    # ground_texture_sim.data_output.write_camera_pose(
    #     config_dict['camera'], config_dict['output'])
    # ground_texture_sim.data_output.write_list_files(
    #     config_dict, trajectory_list)


if __name__ == '__main__':  # pragma: no cover
    main()
