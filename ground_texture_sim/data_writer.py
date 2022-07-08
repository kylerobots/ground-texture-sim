"""!
@brief This module provides a class that writes all the data to the correct files.
"""
import os
from typing import List
import numpy
from ground_texture_sim.name_configuration import NameConfigurator
from ground_texture_sim.transforms import create_transform_matrix


class DataWriter:
    """!
    @brief A class to write properly formatted data, except for images, to each file.
    """

    def __init__(self, output_folder: str, sequence_type: str, sequence_number: str,
                 texture_number: str, camera_name: str) -> None:
        """!
        @brief Construct the DataWriter and ensure the output directory exists.
        @param output_folder The root output folder under which all data resides.
        @param sequence_type A string description of which type of data collection run this is.
        @param sequence_number A unique number, relative to the date and sequence type, to identify
        this particular data collection event.
        @param texture_number An integer representing the texture type mapped.
        @param camera_name The name of the camera in Blender.
        """
        ## The folder all data will be written to.
        self._output_directory = output_folder
        ## The directory to write camera properties
        self._camera_directory = os.path.abspath(
            os.path.join(output_folder, 'camera_properties'))
        # If the directory doesn't already exist, make it.
        if not os.path.exists(self._camera_directory):
            os.makedirs(self._camera_directory)
        ## The name of the camera in Blender
        self._camera_name = camera_name
        ## A class to help with naming things
        self._namer = NameConfigurator(
            output_folder, sequence_type, sequence_number, texture_number, camera_name)

    def _write_array(self, array: numpy.ndarray, file_path: str) -> None:
        """!
        @brief Write a Numpy array to the given file.

        This formats it as one row per line, with spaces as delimiters. Numbers are formatted as
        decimal numbers with 6 places after the decimal.

        @param array The array to write to file. This must be a 2D array.
        @param file_path The file to write to. The path can be absolute or relative. The containing
        folder must exist.
        @return None
        """
        # Create a nicely formatted string first.
        output = ''
        for i in range(array.shape[0]):
            for j in range(array.shape[1]):
                output += F'{array[i, j]:0.6f} '
            # At the end of the row, remove the trailing space and add a newline.
            output = output.strip()
            output += '\n'
        # Now write to file
        with open(file=file_path, mode='w', encoding='utf-8') as file:
            file.write(output)

    def write_camera_intrinsic_matrix(self, camera_intrinsic_matrix: numpy.ndarray) -> None:
        """!
        @brief Write the 3x3 intrinsic matrix to file.

        The file will be called *output*/*camera_name*_intrinsic_matrix.txt and will have one row
        of the matrix per line. Each element is separated by a space.

        @param camera_intrinsic_matrix The 3x3 matrix to write to file.
        @return None
        @exception ValueError raised if the provided matrix is not 3x3.
        """
        if camera_intrinsic_matrix.shape != (3, 3):
            raise ValueError(
                F'Camera matrix must be shape (3,3) not {camera_intrinsic_matrix.shape}')
        file_path = os.path.join(
            self._camera_directory, F'{self._camera_name}_intrinsic_matrix.txt')
        self._write_array(camera_intrinsic_matrix, file_path)

    def write_camera_pose(self, camera_pose: numpy.ndarray) -> None:
        """!
        @brief Write the 4x4 pose matrix to file.

        The file will be called *output*/*camera_name*_pose.txt and will have one row of the matrix
        per line. Each element is separated by a space.

        @param camera_pose The 4x4 matrix to write to file.
        @return None
        @exception ValueError raised if the provided matrix is not 3x3.
        """
        if camera_pose.shape != (4, 4):
            raise ValueError(
                F'Camera matrix must be shape (4,4) not {camera_pose.shape}')
        file_path = os.path.join(
            self._camera_directory, F'{self._camera_name}_pose.txt')
        self._write_array(camera_pose, file_path)

    def write_lists(self, robot_poses: List[List[float]], pixel_poses: List[List[float]]) -> None:
        """!
        @brief Write all the data points in the provided lists to files names according to the data
        format standard.

        The image names are automatically determined, since they follow a consistent format. It is
        assumed that the first element in each list corresponds to the first image, etc.

        @param robot_poses A list of ground truth robot poses, in the form [x, y, yaw]. X and Y are
        in meters and yaw is in radians.
        @param pixel_poses A list of poses for the top left corner of the image, relative to a
        global image aligned with the origin. Each element is in the form [x, y, yaw] where X and Y
        are in pixels and yaw is in radians.
        @return None
        @exception ValueError returned if both lists are not identical in length.
        """
        # Ensure each list is the same size, otherwise, the alternating lists will be screwed up.
        if len(robot_poses) != len(pixel_poses):
            raise ValueError('Provided lists must be the same length.')
        # Derive the list of image paths, making sure a newline will get written.
        image_paths = []
        for i in range(len(robot_poses)):
            image_paths.append(
                self._namer.create_image_path(i, absolute=False) + '\n')
        # Now write each file in turn. Start with the test file, which is just images.
        test_file_path = os.path.join(
            self._output_directory, self._namer.test_file)
        with open(file=test_file_path, mode='w', encoding='utf-8') as test_file:
            for image_path in image_paths:
                test_file.write(image_path)
        # For the next two, alternate with the appropriate pose. Convert the yaw into a matrix.
        meters_txt_file_path = os.path.join(
            self._output_directory, self._namer.meters_txt_file)
        with open(file=meters_txt_file_path, mode='w', encoding='utf-8') as meters_txt_file:
            for image_path, robot_pose in zip(image_paths, robot_poses):
                meters_txt_file.write(image_path)
                # Since there is only a yaw, we can safely extract the upper part of the matrix
                rotation = create_transform_matrix(
                    robot_pose[0], robot_pose[1], 0.0, 0.0, 0.0, robot_pose[2])
                pose_string = F'{rotation[0, 0]:0.6f} {rotation[0, 1]:0.6f} {rotation[0, 3]:0.6f}' \
                    F' {rotation[1, 0]:0.6f} {rotation[1, 1]:0.6f} {rotation[1, 3]:0.6f} ' \
                    F'{0:0.6f} {0:0.6f} {1:0.6f}\n'
                meters_txt_file.write(pose_string)
        txt_file_path = os.path.join(
            self._output_directory, self._namer.txt_file)
        with open(file=txt_file_path, mode='w', encoding='utf-8') as txt_file:
            for image_path, pixel_pose in zip(image_paths, pixel_poses):
                txt_file.write(image_path)
                # Since there is only a yaw, we can safely extract the upper part of the matrix
                rotation = create_transform_matrix(
                    pixel_pose[0], pixel_pose[1], 0.0, 0.0, 0.0, pixel_pose[2])
                pose_string = F'{rotation[0, 0]:0.6f} {rotation[0, 1]:0.6f} {rotation[0, 3]:0.6f}' \
                    F' {rotation[1, 0]:0.6f} {rotation[1, 1]:0.6f} {rotation[1, 3]:0.6f} ' \
                    F'{0:0.6f} {0:0.6f} {1:0.6f}\n'
                txt_file.write(pose_string)
