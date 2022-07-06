"""!
This module tests the blender_interface module.
"""
import unittest
from unittest.mock import MagicMock, patch
import numpy
from ground_texture_sim.blender_interface import BlenderInterface


class TestBlenderInterface(unittest.TestCase):
    """!
    Tests the BlenderInterface class.
    """

    def test_camera_name_default(self) -> None:
        """!
        @brief Tests that the camera name assumes a default value if not specified.
        @return None
        """
        with patch(target='bpy.data') as mock:
            mock.cameras = MagicMock()
            mock.cameras.keys = MagicMock()
            mock.cameras.keys.return_value = ['Camera']
            interface = BlenderInterface()
            self.assertEqual(interface.camera_name, 'Camera',
                             msg='Default camera name not correct.')

    def test_camera_name_invalid(self) -> None:
        """!
        @brief Tests an exception is raised if the provided name doesn't match the one in Blender.
        @return None
        """
        with patch(target='bpy.data') as mock:
            mock.cameras = MagicMock()
            mock.cameras.keys = MagicMock()
            mock.cameras.keys.return_value = ['Camera']
            # Make sure the constructor raises an error.
            with self.assertRaises(NameError,
                                   msg='Constructor does not raise '
                                   'exception on invalid camera name.'):
                _ = BlenderInterface(camera_name='fake_camera')
            # Make sure the setter raises an error.
            interface = BlenderInterface()
            with self.assertRaises(NameError,
                                   msg='Setter does not raise exception on invalid camera name.'):
                interface.camera_name = 'fake_camera'

    def test_camera_name_property(self) -> None:
        """!
        @brief Tests that the getters and setters work.
        @return None
        """
        with patch(target='bpy.data') as mock:
            mock.cameras = MagicMock()
            mock.cameras.keys = MagicMock()
            mock.cameras.keys.return_value = ['c01', 'c55']
            interface = BlenderInterface('c01')
            self.assertEqual(interface.camera_name, 'c01',
                             msg='Camera name not set on construction.')
            interface.camera_name = 'c55'
            self.assertEqual(interface.camera_name, 'c55',
                             msg='Camera name not correctly set.')

    def test_generate_image_relative_path_error(self) -> None:
        """!
        @brief Tests that the generate_image function raises an exception if the image path is not
        absolute.
        @return None
        """
        with patch(target='bpy.data') as mock:
            mock.cameras = MagicMock()
            mock.cameras.keys = MagicMock()
            mock.cameras.keys.return_value = ['Camera']
            with self.assertRaises(ValueError, msg='Relative path does not raise error.'):
                interface = BlenderInterface()
                interface.generate_image(
                    'relative_path/image.png', numpy.identity(4))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
