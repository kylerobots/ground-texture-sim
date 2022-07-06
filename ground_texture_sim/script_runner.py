"""!
The module containing the primary script execution class.
"""
from operator import mod
from typing import List
import ground_texture_sim


class GroundTextureSim():
    """!
    @brief The primary class that executes all data generation.

    This class calls everything else necessary in the module.
    """

    def __init__(self, args: List[str]) -> None:
        """!
        @brief Construct the class, load all configurations, and validate them.
        @param args The command line arguments specified by the user. Generally, this is the result
        of sys.argv
        """
        # Parse the command line arguments
        configs, trajectory = ground_texture_sim.configuration_loader.load_configuration(
            args_list=args)
        # The properly formatted configuration dictionary.
        self._configs = configs
        # The list of trajectories.
        self._trajectory = trajectory
        # The camera pose as specified by the configuration details.
        self._camera_pose = ground_texture_sim.transforms.create_transform_matrix(
            configs['camera']['x'], configs['camera']['y'], configs['camera']['z'],
            configs['camera']['roll'], configs['camera']['pitch'], configs['camera']['yaw']
        )
        # Create any needed classes
        # The interface with blender for the given camera.
        self._blender_interface = ground_texture_sim.blender_interface.BlenderInterface(
            configs['camera']['name'])
        # A class to help with transform math.
        self._transformer = ground_texture_sim.transforms.Transformer(
            self._camera_pose, self._blender_interface.camera_intrinsic_matrix)
        # A class to help with naming things
        self._namer = ground_texture_sim.name_configuration.NameConfigurator(
            configs['output'], configs['sequence']['sequence_type'],
            configs['sequence']['sequence_number'], configs['sequence']['texture_number'],
            configs['camera']['name']
        )

    def run(self) -> None:
        """!
        @brief Generate and write the data to file.
        @return None
        """
        # For each trajectory, convert it into a camera pose and write the image.
        for i, trajectory in enumerate(self._trajectory):
            robot_pose = ground_texture_sim.transforms.create_transform_matrix(
                trajectory[0], trajectory[1], 0.0, 0.0, 0.0, trajectory[2])
            # Convert to a camera pose
            camera_pose = self._transformer.transform_camera_to_world(
                robot_pose)
            # Write camera image
            image_path = self._namer.create_image_path(i, absolute=True)
            self._blender_interface.generate_image(image_path, camera_pose)
                F'{robot_pose[0, 0]:0.6f} {robot_pose[0, 1]:0.6f} {robot_pose[0, 3]:0.6f} {robot_pose[1, 0]:0.6f} {robot_pose[1, 1]:0.6f} {robot_pose[1, 3]:0.6f} 0.0 0.0 1.0\n')
        # Write main list files.
