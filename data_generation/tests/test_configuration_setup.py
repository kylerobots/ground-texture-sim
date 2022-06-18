"""!
This module tests the configuration_setup module.
"""
import unittest
from unittest.mock import mock_open, patch
from json import JSONDecodeError
from math import pi
from data_generation import configuration_setup


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
                KeyError, configuration_setup.load_config, 'trajectory.txt',)

    def test_nonexistent_file(self) -> None:
        """!
        Test the function raises an Exception if the specified file does not
        exist.

        Normally, we mock the file open. However, in this case, we can just
        pass a file that doesn't actually exist and expect the error.

        @return None
        """
        self.assertRaises(FileNotFoundError, configuration_setup.load_config,
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
                JSONDecodeError, configuration_setup.load_config, 'trajectory.txt')

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
            result = configuration_setup.load_config('config.json')
            self.assertDictEqual(d1=result, d2=expected_results,
                                 msg='Optional values not filled in.')
        # Test if no options are provided.
        input_string = '{\n"trajectory": "trajectory.txt",\n"output": "output/"\n}'
        expected_results['camera_properties']['x'] = 0.0
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = configuration_setup.load_config('config.json')
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
            result = configuration_setup.load_config('config.json')
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
            result = configuration_setup.load_trajectory('trajectory.txt')
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
                          configuration_setup.load_trajectory, 'non_a_real_file.txt')

    def test_not_full_pose(self) -> None:
        """!
        This method verifies that the function throws an exception if any of the
        poses do not define all three numbers (X, Y, and Yaw)

        @return None
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(
                RuntimeError, configuration_setup.load_trajectory, 'trajectory.txt')
        input_string = '0.0,0.0\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(
                RuntimeError, configuration_setup.load_trajectory, 'trajectory.txt')

    def test_not_numbers(self) -> None:
        """!
        This method verifies that the function throws an exception if any of
        the poses are not composed of numbers.

        @return None
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,the\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(
                RuntimeError, configuration_setup.load_trajectory, 'trajectory.txt')

    def test_no_whitespace(self) -> None:
        """!
        This method verifies that reading poses from files works even without
        whitespace between the numbers.

        @return None
        """
        input_string = '0.0,0.0,0.0\n1.0,2.0,3.0'
        expected_result = [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]]
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            results = configuration_setup.load_trajectory('trajectory.txt')
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
            results = configuration_setup.load_trajectory('trajectory.txt')
            self.assertListEqual(list1=results, list2=expected_results,
                                 msg='Poses not successfully read from file.')
