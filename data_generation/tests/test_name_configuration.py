"""!
This module tests the name_configuration module
"""
import unittest
import datetime
from os import path
from data_generation import name_configuration


class TestCreateImagePath(unittest.TestCase):
    """!
    This class tests the create_image_path function.
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
            input_dict['output'], 'regular', current_date.strftime('%y%m%d'), 'seq0003')
        base_directory = path.abspath(base_directory)
        file_name = F'HDG2_t002_regular_{current_date.strftime("%Y-%m-%d")}_s0003_c01_i0000005.png'
        expected_result = path.join(base_directory, file_name)
        actual_result = name_configuration.create_image_path(
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
            input_dict['output'], 'regular', current_date.strftime('%y%m%d'), 'seq0003')
        base_directory = path.abspath(base_directory)
        file_name = F'HDG2_t002_regular_{current_date.strftime("%Y-%m-%d")}_s0003_c01_i0000005.png'
        expected_result = path.join(base_directory, file_name)
        actual_result = name_configuration.create_image_path(
            image_number, input_dict)
        self.assertEqual(expected_result, actual_result,
                         msg='Image string is not correct')


class TestCreateFileListBase(unittest.TestCase):
    """!
    This class tests the create_file_list_base function.
    """

    def test_success(self) -> None:
        """!
        Assuming a well-formed configuration dictionary, test that the base name follows the
        expected format.

        The name should be "<sequence_type>_<date in YYMMDD>

        @return None
        """
        # Create a dictionary with the minimum required values needed for the function.
        configs = {
            "output": "output",
            "sequence": {
                "texture_number": 1,
                "sequence_type": "regular_test",
                "sequence_number": 1
            }
        }
        current_date = datetime.date.today()
        expected_result = F'regular_test_{current_date.strftime("%y%m%d")}'
        result = name_configuration.create_file_list_base(configs)
        self.assertEqual(result, expected_result,
                         msg='Main file list names are not correct')
