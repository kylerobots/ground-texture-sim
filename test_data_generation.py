"""!
This module provides the unit tests for the data_generation module.

SPDX-License-Identifier: GPL-3.0-or-later
"""
from json import JSONDecodeError
from math import pi
from unittest.mock import mock_open, patch
import unittest
import data_generation


class TestLoadConfig(unittest.TestCase):
    """!
    This class tests the load_config function.
    """

    def test_missing_required_entries(self) -> None:
        """!
        Test the function raises an Exception if required entries are not
        present.

        At a minimum, the JSON should specify the output directory and the
        trajectory file.

        @return None
        """
        input_string = '{\n"trajectory": "trajectory.txt",\n"gpu": true\n}'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(
                KeyError, data_generation.load_config, 'trajectory.txt',)

    def test_nonexistent_file(self) -> None:
        """!
        Test the function raises an Exception if the specified file does not
        exist.

        Normally, we mock the file open. However, in this case, we can just
        pass a file that doesn't actually exist and expect the error.

        @return None
        """
        self.assertRaises(FileNotFoundError, data_generation.load_config,
                          'non_a_real_file.json')

    def test_not_json(self) -> None:
        """!
        Test the function raises an Exception if the specified file is not in
        JSON format.

        @return None
        """
        input_string = 'not a json\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(
                JSONDecodeError, data_generation.load_config, 'trajectory.txt')

    def test_optional_missing(self) -> None:
        """!
        Test the function includes optional values if not found in the specified file.

        @return None
        """
        # Test if only some optional values are provided.
        input_string = '{\n"trajectory": "trajectory.txt",\n"output": "output/"' \
            ',\n"camera_properties": {\n"x": 1.0\n}\n}'
        expected_results = {
            'output': 'output/',
            'trajectory': 'trajectory.txt',
            'camera_properties': {
                'x': 1.0,
                'y': 0.0,
                'z': 0.0,
                'roll': 0.0,
                'pitch': pi / 2.0,
                'yaw': 0.0
            }
        }
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = data_generation.load_config('config.json')
            self.assertDictEqual(d1=result, d2=expected_results,
                                 msg='Optional values not filled in.')
        # Test if no options are provided.
        input_string = '{\n"trajectory": "trajectory.txt",\n"output": "output/"\n}'
        expected_results['camera_properties']['x'] = 0.0
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = data_generation.load_config('config.json')
            self.assertDictEqual(d1=result, d2=expected_results,
                                 msg='Optional values not filled in.')

    def test_successful(self) -> None:
        """!
        Test the function works as expected if the specified file is correct.

        @return None
        """
        input_string = '{\n"trajectory": "trajectory.txt",\n"output": "output/"' \
            ',\n"camera_properties": {\n"x": 1.0,\n"y": 2.0,\n"z": 3.0,\n"roll": 0.0,\n' \
            '"pitch": 1.0,\n"yaw": 2.0\n}\n}'
        expected_results = {
            'output': 'output/',
            'trajectory': 'trajectory.txt',
            'camera_properties': {
                'x': 1.0,
                'y': 2.0,
                'z': 3.0,
                'roll': 0.0,
                'pitch': 1.0,
                'yaw': 2.0
            }
        }
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = data_generation.load_config('config.json')
            self.assertDictEqual(d1=result, d2=expected_results,
                                 msg='Unable to read JSON into Dict')


class TestLoadTrajectory(unittest.TestCase):
    """!
    This class tests the read_poses function.
    """

    def test_empty_file(self) -> None:
        """!
        This method verifies that the function returns an empty list if the file
        is empty.

        @return None
        """
        input_string = '\n\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = data_generation.load_trajectory('trajectory.txt')
            self.assertEqual(len(result), 0)

    def test_nonexistent_file(self) -> None:
        """!
        This method verifies that the function throws an exception if the
        provided file does not exist.

        Normally, we mock the file open. However, in this case, we can just
        pass a file that doesn't actually exist and expect the error.

        @return None
        """
        self.assertRaises(FileNotFoundError,
                          data_generation.load_trajectory, 'non_a_real_file.txt')

    def test_not_full_pose(self) -> None:
        """!
        This method verifies that the function throws an exception if any of the
        poses do not define all three numbers (X, Y, and Yaw)

        @return None
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(
                RuntimeError, data_generation.load_trajectory, 'trajectory.txt')
        input_string = '0.0,0.0\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(
                RuntimeError, data_generation.load_trajectory, 'trajectory.txt')

    def test_not_numbers(self) -> None:
        """!
        This method verifies that the function throws an exception if any of
        the poses are not composed of numbers.

        @return None
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,the\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(
                RuntimeError, data_generation.load_trajectory, 'trajectory.txt')

    def test_no_whitespace(self) -> None:
        """!
        This method verifies that reading poses from files works even without
        whitespace between the numbers.

        @return None
        """
        input_string = '0.0,0.0,0.0\n1.0,2.0,3.0'
        expected_result = [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]]
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            results = data_generation.load_trajectory('trajectory.txt')
            self.assertListEqual(list1=results, list2=expected_result,
                                 msg='Poses not successfully read from file.')

    def test_with_whitespace(self) -> None:
        """!
        This method verifies that reading poses from files can appropriately
        strip whitespace when reading.

        @return None
        """
        input_string = '0.0, 0.0, 0.0\n1.0, 2.0, 3.0\n\n'
        expected_results = [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]]
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            results = data_generation.load_trajectory('trajectory.txt')
            self.assertListEqual(list1=results, list2=expected_results,
                                 msg='Poses not successfully read from file.')


class TestParseArgs(unittest.TestCase):
    """!
    This class tests the parse_args function.
    """

    def test_help_flag(self) -> None:
        """!
        Test that the system exists if the -h flag is passed.

        @return None
        """
        args = ['blender', '--python',
                'data_generation.py', '-b', '--', '-h']
        self.assertRaises(SystemExit, data_generation.parse_args, args)

    def test_no_args(self) -> None:
        """!
        Test that the system exists if no JSON file is provided.

        @return None
        """
        args = ['blender', '--python', 'data_generation.py', '-b']
        self.assertRaises(SystemExit, data_generation.parse_args, args)

    def test_too_many_args(self) -> None:
        """!
        Test that the system exists if too many arguments are present.

        @return None
        """
        args = ['blender', '--python', 'data_generation.py',
                '-b', '--', 'config.json', 'other_config.json']
        self.assertRaises(SystemExit, data_generation.parse_args, args)

    def test_with_filename(self) -> None:
        """!
        Test that the argument for the JSON is correctly parsed.

        @return None
        """
        args = ['blender', '--python',
                'data_generation.py', '-b', '--', 'config.json']
        result = data_generation.parse_args(args)
        self.assertEqual(result, 'config.json',
                         msg='Unable to successfully extract JSON file.')


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
            data_generation.write_camera_pose(
                'camera_pose.txt', camera_properties)
            mock.assert_called_once_with(
                file='camera_pose.txt', mode='w', encoding='utf8')
            mock().write.assert_called_once_with(expected_output)

    def test_example(self) -> None:
        """!
        This method verifies the output correctly assembles a homogenous
        transform.

        @return None
        """
        camera_properties = {
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
            data_generation.write_camera_pose(
                'camera_pose.txt', camera_properties)
            mock.assert_called_once_with(
                file='camera_pose.txt', mode='w', encoding='utf8')
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
            data_generation.write_trajectory('trajectory.txt', trajectory)
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
            data_generation.write_trajectory('trajectory.txt', trajectory)
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
                self.assertRaises(RuntimeError, data_generation.write_trajectory,
                                  'trajectory.txt', trajectory)
                mock.assert_not_called()


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
