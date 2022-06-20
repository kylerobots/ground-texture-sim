"""!
This module tests the data_output module.
"""
from math import pi
from os import getcwd
from unittest.mock import mock_open, patch
import unittest
from data_generation import data_output


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
            data_output.write_camera_pose(camera_properties, getcwd())
            mock.assert_called_once_with(
                file=F'{getcwd()}/camera_properties/camera_pose.txt', mode='w', encoding='utf8')
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
            data_output.write_camera_pose(camera_properties, getcwd())
            mock.assert_called_once_with(
                file=F'{getcwd()}/camera_properties/c15_pose.txt', mode='w', encoding='utf8')
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
