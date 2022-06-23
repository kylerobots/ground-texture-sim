"""!
This module tests the blender_interface module.
"""
import datetime
import unittest
from os import path
from data_generation.blender_interface import _create_image_path


class TestCreateImagePath(unittest.TestCase):
    """!
    This class tests the _create_image_path function.
    """

    def test_success_absolute(self) -> None:
        """!
        Test that the function creates the expected path when the output is an absolute directory.

        @return None
        """
        input_dict = {
            'camera': {
                'name': 'c01'
            },
            'output': '/opt',
            'sequence': {
                'texture_number': 2,
                'sequence_number': 3,
                'sequence_type': 'regular'
            }
        }
        image_number = 5
        current_date = datetime.date.today()
        base_directory = path.join(
            input_dict['output'], 'regular', current_date.strftime('%y%m%d'), 'seq003')
        base_directory = path.abspath(base_directory)
        file_name = F'HDG2_t002_regular_{current_date.strftime("%Y-%m-%d")}_s0003_c01_i0000005.png'
        expected_result = path.join(base_directory, file_name)
        actual_result = _create_image_path(
            image_number, input_dict)
        self.assertEqual(expected_result, actual_result,
                         msg='Image string is not correct')

    def test_success_relative(self) -> None:
        """!
        Test the function creates the expected path when the output is a relative directory.

        @return None
        """
        input_dict = {
            'output': 'output',
            'camera': {
                'name': 'c01'
            },
            'sequence': {
                'texture_number': 2,
                'sequence_number': 3,
                'sequence_type': 'regular'
            }
        }
        image_number = 5
        current_date = datetime.date.today()
        base_directory = path.join(
            input_dict['output'], 'regular', current_date.strftime('%y%m%d'), 'seq003')
        base_directory = path.abspath(base_directory)
        file_name = F'HDG2_t002_regular_{current_date.strftime("%Y-%m-%d")}_s0003_c01_i0000005.png'
        expected_result = path.join(base_directory, file_name)
        actual_result = _create_image_path(
            image_number, input_dict)
        self.assertEqual(expected_result, actual_result,
                         msg='Image string is not correct')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
