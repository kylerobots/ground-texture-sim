"""!
This module provides the unit tests for the generate_data module.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import unittest
import generate_data


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
        self.assertRaises(SystemExit, generate_data.parse_args, args)

    def test_no_args(self) -> None:
        """!
        Test that the system exists if no JSON file is provided.

        @return None
        """
        args = ['blender', '--python', 'generate_data.py', '-b']
        self.assertRaises(SystemExit, generate_data.parse_args, args)

    def test_too_many_args(self) -> None:
        """!
        Test that the system exists if too many arguments are present.

        @return None
        """
        args = ['blender', '--python', 'generate_data.py',
                '-b', '--', 'config.json', 'other_config.json']
        self.assertRaises(SystemExit, generate_data.parse_args, args)

    def test_with_filename(self) -> None:
        """!
        Test that the argument for the JSON is correctly parsed.

        @return None
        """
        args = ['blender', '--python',
                'generate_data.py', '-b', '--', 'config.json']
        result = generate_data.parse_args(args)
        self.assertEqual(result, 'config.json',
                         msg='Unable to successfully extract JSON file.')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
