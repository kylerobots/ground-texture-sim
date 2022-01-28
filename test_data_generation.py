"""
This module provides the unit tests for the data_generation module.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import unittest
from unittest.mock import mock_open, patch
from data_generation import read_poses


class TestReadPoses(unittest.TestCase):
    """
    This class tests the read_poses function.
    """

    def test_empty_file(self) -> None:
        """
        This method verifies that the function returns an empty list if the file
        is empty.
        """
        input_string = '\n\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = read_poses('trajectory.txt')
            self.assertEqual(len(result), 0)

    def test_nonexistent_file(self) -> None:
        """
        This method verifies that the function throws an exception if the
        provided file does not exist.

        Normally, we mock the file open. However, in this case, we can just
        pass a file that doesn't actually exist and expect the error.
        """
        self.assertRaises(FileNotFoundError, read_poses, 'non_a_real_file.txt')

    def test_not_full_pose(self) -> None:
        """
        This method verifies that the function throws an exception if any of the
        poses do not define all three numbers (X, Y, and Yaw)
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(RuntimeError, read_poses, 'trajectory.txt')

    def test_not_numbers(self) -> None:
        """
        This method verifies that the function throws an exception if any of
        the poses are not composed of numbers.
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,the\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(RuntimeError, read_poses, 'trajectory.txt')

    def test_no_whitespace(self) -> None:
        """
        This method verifies that reading poses from files works even without
        whitespace between the numbers.
        """
        input_string = '0.0,0.0,0.0\n1.0,2.0,3.0'
        expected_result = [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]]
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            results = read_poses('trajectory.txt')
            self.assertListEqual(list1=results, list2=expected_result,
                                 msg='Poses not successfully read from file.')

    def test_with_whitespace(self) -> None:
        """
        This method verifies that reading poses from files can appropriately
        strip whitespace when reading.
        """
        input_string = '0.0, 0.0, 0.0\n1.0, 2.0, 3.0\n\n'
        expected_results = [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]]
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            results = read_poses('trajectory.txt')
            self.assertListEqual(list1=results, list2=expected_results,
                                 msg='Poses not successfully read from file.')


if __name__ == '__main__':
    unittest.main()
