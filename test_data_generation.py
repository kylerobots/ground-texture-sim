"""!
This module provides the unit tests for the data_generation module.

SPDX-License-Identifier: GPL-3.0-or-later
"""
from json import JSONDecodeError
import unittest
from unittest.mock import mock_open, patch
from data_generation import parse_args, read_config, read_poses


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
        self.assertRaises(SystemExit, parse_args, args)

    def test_no_args(self) -> None:
        """!
        Test that the system exists if no JSON file is provided.

        @return None
        """
        args = ['blender', '--python', 'data_generation.py', '-b']
        self.assertRaises(SystemExit, parse_args, args)

    def test_too_many_args(self) -> None:
        """!
        Test that the system exists if too many arguments are present.

        @return None
        """
        args = ['blender', '--python', 'data_generation.py',
                '-b', '--', 'config.json', 'other_config.json']
        self.assertRaises(SystemExit, parse_args, args)

    def test_with_filename(self) -> None:
        """!
        Test that the argument for the JSON is correctly parsed.

        @return None
        """
        args = ['blender', '--python',
                'data_generation.py', '-b', '--', 'config.json']
        result = parse_args(args)
        self.assertEqual(result, 'config.json',
                         msg='Unable to successfully extract JSON file.')


class TestReadConfig(unittest.TestCase):
    """!
    This class tests the read_config function.
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
            self.assertRaises(KeyError, read_config, 'trajectory.txt',)

    def test_nonexistent_file(self) -> None:
        """!
        Test the function raises an Exception if the specified file does not
        exist.

        Normally, we mock the file open. However, in this case, we can just
        pass a file that doesn't actually exist and expect the error.

        @return None
        """
        self.assertRaises(FileNotFoundError, read_config,
                          'non_a_real_file.json')

    def test_not_json(self) -> None:
        """!
        Test the function raises an Exception if the specified file is not in
        JSON format.

        @return None
        """
        input_string = 'not a json\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(JSONDecodeError, read_config, 'trajectory.txt')

    def test_successful(self) -> None:
        """!
        Test the function works as expected if the specified file is correct.

        @return None
        """
        input_string = '{\n"trajectory": "trajectory.txt",\n"output": "output/"' \
            ',\n"camera height": 1.0,\n"gpu": true\n}'
        expected_result = {
            'output': 'output/',
            'trajectory': 'trajectory.txt',
            'camera height': 1.0,
            'gpu': True
        }
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = read_config('config.json')
            self.assertDictEqual(d1=result, d2=expected_result,
                                 msg='Unable to read JSON into Dict')


class TestReadPoses(unittest.TestCase):
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
            result = read_poses('trajectory.txt')
            self.assertEqual(len(result), 0)

    def test_nonexistent_file(self) -> None:
        """!
        This method verifies that the function throws an exception if the
        provided file does not exist.

        Normally, we mock the file open. However, in this case, we can just
        pass a file that doesn't actually exist and expect the error.

        @return None
        """
        self.assertRaises(FileNotFoundError, read_poses, 'non_a_real_file.txt')

    def test_not_full_pose(self) -> None:
        """!
        This method verifies that the function throws an exception if any of the
        poses do not define all three numbers (X, Y, and Yaw)

        @return None
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(RuntimeError, read_poses, 'trajectory.txt')
        input_string = '0.0,0.0\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(RuntimeError, read_poses, 'trajectory.txt')

    def test_not_numbers(self) -> None:
        """!
        This method verifies that the function throws an exception if any of
        the poses are not composed of numbers.

        @return None
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,the\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(RuntimeError, read_poses, 'trajectory.txt')

    def test_no_whitespace(self) -> None:
        """!
        This method verifies that reading poses from files works even without
        whitespace between the numbers.

        @return None
        """
        input_string = '0.0,0.0,0.0\n1.0,2.0,3.0'
        expected_result = [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]]
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            results = read_poses('trajectory.txt')
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
            results = read_poses('trajectory.txt')
            self.assertListEqual(list1=results, list2=expected_results,
                                 msg='Poses not successfully read from file.')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
