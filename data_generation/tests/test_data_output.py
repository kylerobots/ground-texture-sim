"""!
This module tests the data_output module.
"""
from math import pi
from unittest.mock import mock_open, patch
import unittest
from data_generation import data_output


class TestPrepareOutputFolder(unittest.TestCase):
    """!
    This class verifies that the prepare_output_folder function works.
    """

    def test_exists(self) -> None:
        """!
        This verifies nothing happens if the folders already exist.

        @return None
        """
        with patch('os.path.exists') as mock_exist:
            mock_exist.return_value = True
            with patch('os.makedirs') as mock_make:
                data_output.prepare_output_folder('/fake_dir')
                mock_exist.assert_called_once_with(
                    '/fake_dir/camera_properties')
                mock_make.assert_not_called()

    def test_not_exist(self) -> None:
        """!
        This method verifies the directory is created if neither the output nor subdirectory exists.

        @return None
        """
        with patch(target='os.makedirs') as mock:
            data_output.prepare_output_folder('/fake_dir')
            mock.assert_called_once_with('/fake_dir/camera_properties')

    def test_root_exists(self) -> None:
        """!
        This method verifies the subfolder directory is created if it doesn't exist.

        @return None
        """
        with patch(target='os.makedirs') as mock:
            data_output.prepare_output_folder('/opt/')
            mock.assert_called_once_with('/opt/camera_properties')


class TestWriteCameraPose(unittest.TestCase):
    """!
    This class verifies that the camera pose is written as a homogenous matrix
    to file.
    """

    def test_identity(self) -> None:
        """!
        This method verifies the correct identity matrix is written.

        @return None
        """
        camera_properties = {
            'name': 'camera',
            'x': 0.0,
            'y': 0.0,
            'z': 0.0,
            'roll': 0.0,
            'pitch': 0.0,
            'yaw': 0.0
        }
        expected_output = '1.000000, 0.000000, 0.000000, 0.000000\n' \
            '0.000000, 1.000000, 0.000000, 0.000000\n' \
            '-0.000000, 0.000000, 1.000000, 0.000000\n' \
            '0.000000, 0.000000, 0.000000, 1.000000\n'
        with patch(target='builtins.open', new=mock_open()) as mock:
            data_output.write_camera_pose(camera_properties, '/output_folder')
            mock.assert_called_once_with(
                file='/output_folder/camera_properties/camera_pose.txt', mode='w', encoding='utf8')
            mock().write.assert_called_once_with(expected_output)

    def test_example(self) -> None:
        """!
        This method verifies the output correctly assembles a homogenous
        transform.

        @return None
        """
        camera_properties = {
            'name': 'c15',
            'x': 1.0,
            'y': 2.0,
            'z': 3.0,
            'roll': pi / 2.0,
            'pitch': -pi / 2.0,
            'yaw': pi
        }
        expected_output = '-0.000000, 1.000000, 0.000000, 1.000000\n' \
            '0.000000, -0.000000, 1.000000, 2.000000\n' \
            '1.000000, 0.000000, 0.000000, 3.000000\n' \
            '0.000000, 0.000000, 0.000000, 1.000000\n'
        with patch(target='builtins.open', new=mock_open()) as mock:
            data_output.write_camera_pose(camera_properties, 'output_folder')
            mock.assert_called_once_with(
                file='output_folder/camera_properties/c15_pose.txt', mode='w', encoding='utf8')
            mock().write.assert_called_once_with(expected_output)


class TestWriteTrajectory(unittest.TestCase):
    """!
    This class verifies that the trajectory is written to file correctly.
    """

    def test_empty_list(self) -> None:
        """!
        This method verifies an empty file is written if the provided trajectory
        is empty.

        @return None
        """
        trajectory = []
        with patch(target='builtins.open', new=mock_open()) as mock:
            data_output.write_trajectory('trajectory.txt', trajectory)
            mock.assert_called_once_with(
                file='trajectory.txt', mode='w', encoding='utf8')
            mock().write.assert_called_once_with('')

    def test_success(self) -> None:
        """!
        This method verifies the correct file format is written when provided an expected response.

        @return None
        """
        trajectory = [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]
        expected_output = '0.000000, 0.000000, 0.000000\n1.000000, 1.000000, 1.000000\n'
        with patch(target='builtins.open', new=mock_open()) as mock:
            data_output.write_trajectory('trajectory.txt', trajectory)
            mock.assert_called_once_with(
                file='trajectory.txt', mode='w', encoding='utf8')
            mock().write.assert_called_once_with(expected_output)

    def test_wrong_type(self) -> None:
        """!
        This method verifies nothing is written if the list is poorly formed.

        @return None
        """
        trajectory_string = [[0.0, 0.0, 0.0], ['1.0', 1.0, 1.0]]
        trajectory_length = [[0.0, 0.0, 0.0], [1.0, 1.0]]
        bad_trajectories = [trajectory_string, trajectory_length]
        with patch(target='builtins.open', new=mock_open()) as mock:
            for trajectory in bad_trajectories:
                self.assertRaises(RuntimeError, data_output.write_trajectory,
                                  'trajectory.txt', trajectory)
                mock.assert_not_called()


if __name__ == '__main__':
    unittest.main()
