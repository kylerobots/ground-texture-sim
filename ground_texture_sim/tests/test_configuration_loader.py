"""!
This module tests the configuration_loader module.
"""
import json
import unittest
from typing import Dict
from unittest.mock import mock_open, patch
from ground_texture_sim.configuration_loader import _load_config, _load_trajectory, _parse_args


class TestLoadConfig(unittest.TestCase):
    """!
    This class tests the load_config function.
    """

    def _create_correct_config(self, include_options: bool = True) -> Dict:
        """!
        A helper function to create correctly formatted Dicts, with or without options.

        @param include_options Whether or not to include all optional keys with default values.
        @return The Dict
        """
        result = {
            'camera': {
                'name': 'Camera'
            },
            'output': 'output/',
            'sequence': {
                'sequence_number': 1,
                'sequence_type': 'regular',
                'texture_number': 1
            },
            'trajectory': 'trajectory.txt'
        }
        if include_options:
            result['camera']['x'] = 0.0
            result['camera']['y'] = 0.0
            result['camera']['z'] = 0.0
            result['camera']['roll'] = 0.0
            result['camera']['pitch'] = 1.5708
            result['camera']['yaw'] = 0.0
        return result

    def _dict_to_string(self, input_dict: Dict) -> str:
        """!
        A helper function to convert Dicts to correctly formatted JSON strings.

        @param input_dict The dictionary to format as a JSON string.
        @return A JSON string
        """
        return json.dumps(input_dict, indent=4)

    def test_missing_camera_elements(self) -> None:
        """!
        Test that the camera name must be included in the user provided JSON.

        @return None
        """
        # Name must be specified
        input_dict = self._create_correct_config(True)
        input_dict['camera'].pop('name')
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(KeyError, _load_config, 'config.json',)
        # Camera must also be specified
        input_dict.pop('camera')
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(KeyError, _load_config, 'config.json',)

    def test_missing_sequence_elements(self) -> None:
        """!
        Test that all required sequence keys are checked for.

        @return None
        """
        # Texture number
        input_dict = self._create_correct_config(True)
        input_dict['sequence'].pop('texture_number')
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(KeyError, _load_config, 'config.json',)
        # Sequence type
        input_dict = self._create_correct_config(True)
        input_dict['sequence'].pop('sequence_type')
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(KeyError, _load_config, 'config.json',)
        # Sequence number
        input_dict = self._create_correct_config(True)
        input_dict['sequence'].pop('sequence_number')
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(KeyError, _load_config, 'config.json',)

    def test_missing_top_levels(self) -> None:
        """!
        Test the function raises an Exception if certain required entries are not present.

        This ensures that 'trajectory' and 'output' are both required.

        @return None
        """
        # Test that trajectory must be there.
        input_dict = self._create_correct_config(True)
        input_dict.pop('trajectory')
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(KeyError, _load_config, 'config.json',)
        input_dict = self._create_correct_config(True)
        input_dict.pop('output')
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(KeyError, _load_config, 'config.json',)

    def test_nonexistent_file(self) -> None:
        """!
        Test the function raises an Exception if the specified file does not
        exist.

        Normally, we mock the file open. However, in this case, we can just
        pass a file that doesn't actually exist and expect the error.

        @return None
        """
        self.assertRaises(FileNotFoundError, _load_config,
                          'non_a_real_file.json')

    def test_not_json(self) -> None:
        """!
        Test the function raises an Exception if the specified file is not in
        JSON format.

        @return None
        """
        input_string = 'not a json\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(json.JSONDecodeError,
                              _load_config, 'config.json')

    def test_optional_missing(self) -> None:
        """!
        Test the function includes optional values if not found in the specified file.

        @return None
        """
        # Test if no optional values are provided.
        input_dict = self._create_correct_config(False)
        expected_results = self._create_correct_config(True)
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = _load_config('config.json')
            self.assertDictEqual(d1=result, d2=expected_results,
                                 msg='Optional values not filled in.')
        # Test if only some options are provided
        input_dict['camera']['x'] = 5.0
        expected_results['camera']['x'] = 5.0
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = _load_config('config.json')
            self.assertDictEqual(d1=result, d2=expected_results,
                                 msg='Optional values not filled in.')

    def test_sequence_number_is_number(self) -> None:
        """!
        Test the loader verifies the sequence number is an actual number.

        @return None
        """
        input_dict = self._create_correct_config(True)
        # Switch to a string
        input_dict['sequence']['sequence_number'] = "blah"
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(TypeError, _load_config, 'config.json')
        # Floats aren't supported either
        input_dict['sequence']['sequence_number'] = "2.1"
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(TypeError, _load_config, 'config.json')
        # Strings that can convert to ints are fine though
        input_dict['sequence']['sequence_number'] = "2"
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = _load_config('config.json')
            self.assertEqual(result['sequence']['sequence_number'], 2)

    def test_successful(self) -> None:
        """!
        Test the function works as expected if the specified file is correct.

        @return None
        """
        input_dict = self._create_correct_config(True)
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = _load_config('config.json')
            self.assertDictEqual(d1=result, d2=input_dict,
                                 msg='Unable to read JSON into Dict')

    def test_texture_number_is_number(self) -> None:
        """!
        Test the loader verifies the sequence number is an actual number.

        @return None
        """
        input_dict = self._create_correct_config(True)
        # Switch to a string
        input_dict['sequence']['texture_number'] = "blah"
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(TypeError, _load_config, 'config.json')
        # Floats aren't supported either
        input_dict['sequence']['texture_number'] = "2.1"
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(TypeError, _load_config, 'config.json')
        # Strings that can convert to ints are fine though
        input_dict['sequence']['texture_number'] = "2"
        input_string = self._dict_to_string(input_dict)
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            result = _load_config('config.json')
            self.assertEqual(result['sequence']['texture_number'], 2)


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
            result = _load_trajectory('trajectory.txt')
            self.assertEqual(len(result), 0)

    def test_nonexistent_file(self) -> None:
        """!
        This method verifies that the function throws an exception if the
        provided file does not exist.

        Normally, we mock the file open. However, in this case, we can just
        pass a file that doesn't actually exist and expect the error.

        @return None
        """
        self.assertRaises(FileNotFoundError, _load_trajectory,
                          'non_a_real_file.txt')

    def test_not_full_pose(self) -> None:
        """!
        This method verifies that the function throws an exception if any of the
        poses do not define all three numbers (X, Y, and Yaw)

        @return None
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(RuntimeError, _load_trajectory, 'trajectory.txt')
        input_string = '0.0,0.0\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(RuntimeError, _load_trajectory, 'trajectory.txt')

    def test_not_numbers(self) -> None:
        """!
        This method verifies that the function throws an exception if any of
        the poses are not composed of numbers.

        @return None
        """
        input_string = '0.0,0.0,0.0\n0.0,0.0,the\n'
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            self.assertRaises(RuntimeError, _load_trajectory, 'trajectory.txt')

    def test_no_whitespace(self) -> None:
        """!
        This method verifies that reading poses from files works even without
        whitespace between the numbers.

        @return None
        """
        input_string = '0.0,0.0,0.0\n1.0,2.0,3.0'
        expected_result = [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]]
        with patch(target='builtins.open', new=mock_open(read_data=input_string)):
            results = _load_trajectory('trajectory.txt')
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
            results = _load_trajectory('trajectory.txt')
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
                'generate_data.py', '-b', '--', '-h']
        self.assertRaises(SystemExit, _parse_args, args)

    def test_no_args(self) -> None:
        """!
        Test that the system exists if no JSON file is provided.

        @return None
        """
        args = ['blender', '--python', 'generate_data.py', '-b']
        self.assertRaises(SystemExit, _parse_args, args)

    def test_too_many_args(self) -> None:
        """!
        Test that the system exists if too many arguments are present.

        @return None
        """
        args = ['blender', '--python', 'generate_data.py',
                '-b', '--', 'config.json', 'other_config.json']
        self.assertRaises(SystemExit, _parse_args, args)

    def test_with_filename(self) -> None:
        """!
        Test that the argument for the JSON is correctly parsed.

        @return None
        """
        args = ['blender', '--python',
                'generate_data.py', '-b', '--', 'config.json']
        result = _parse_args(args)
        self.assertEqual(result, 'config.json',
                         msg='Unable to successfully extract JSON file.')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
