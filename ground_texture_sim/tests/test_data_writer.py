"""!
@brief This module provides tests for the data_writer module.
"""
import datetime
import unittest
from unittest.mock import mock_open, patch
import numpy
from ground_texture_sim.data_writer import DataWriter


class TestDataWriter(unittest.TestCase):
    """!
    @brief Tests the DataWriter class.
    """

    def test_list_writing(self) -> None:
        """!
        @brief Test that the list files are well formed and written to the correct spot.
        @return None
        """
        # Create inputs and expected outputs.
        date_folder = datetime.date.today().strftime("%y%m%d")
        date_file = datetime.date.today().strftime("%Y-%m-%d")
        expected_image_strings = [
            F'regular/{date_folder}/seq0003/HDG2_t001_regular_{date_file}_s0003_c55_i0000000.png\n',
            F'regular/{date_folder}/seq0003/HDG2_t001_regular_{date_file}_s0003_c55_i0000001.png\n'
        ]
        meters_inputs = [
            [0.0, 0.0, 0.0],
            [1.0, 2.0, numpy.pi / 2.0]
        ]
        expected_meters_strings = [
            F'{1:0.6f} {0:0.6f} {0:0.6f} {0:0.6f} {1:0.6f} {0:0.6f} {0:0.6f} {0:0.6f} {1:0.6f}\n',
            F'{0:0.6f} {-1:0.6f} {1:0.6f} {1:0.6f} {0:0.6f} {2:0.6f} {0:0.6f} {0:0.6f} {1:0.6f}\n'
        ]
        pixels_inputs = [
            [0.0, 0.0, 0.0],
            [5.0, 4.0, numpy.pi / 2.0]
        ]
        expected_pixels_strings = [
            F'{1:0.6f} {0:0.6f} {0:0.6f} {0:0.6f} {1:0.6f} {0:0.6f} {0:0.6f} {0:0.6f} {1:0.6f}\n',
            F'{0:0.6f} {-1:0.6f} {5:0.6f} {1:0.6f} {0:0.6f} {4:0.6f} {0:0.6f} {0:0.6f} {1:0.6f}\n'
        ]
        # Also create the expected file names that are being written to.
        # Create the expected file names
        datestring = datetime.date.today().strftime('%y%m%d')
        test_string = F'/output/regular_{datestring}.test'
        txt_string = F'/output/regular_{datestring}.txt'
        meters_txt_string = F'/output/regular_{datestring}_meters.txt'
        # Write the stuff
        with patch('os.path.exists') as mock_exist:
            mock_exist.return_value = True
            writer = DataWriter('/output', 'regular', 3, 1, 'c55')
            with patch(target='builtins.open', new=mock_open()) as mock_output:
                writer.write_lists(meters_inputs, pixels_inputs)
                # Verify the right files are opened.
                mock_output.assert_any_call(
                    file=test_string, mode='w', encoding='utf-8')
                mock_output.assert_any_call(
                    file=txt_string, mode='w', encoding='utf-8')
                mock_output.assert_any_call(
                    file=meters_txt_string, mode='w', encoding='utf-8')
                # Verify the information is written. However, this will not verify the correct order
                # or correct file.
                mock_output().write.assert_any_call(expected_image_strings[0])
                mock_output().write.assert_any_call(expected_image_strings[1])
                mock_output().write.assert_any_call(expected_meters_strings[0])
                mock_output().write.assert_any_call(expected_meters_strings[1])
                mock_output().write.assert_any_call(expected_pixels_strings[0])
                mock_output().write.assert_any_call(expected_pixels_strings[1])

    def test_list_writing_mismatched_sizes(self) -> None:
        """!
        @brief Ensure an exception is raised if there is not an even number of images, ground, and
        pixel values.
        @return None
        """
        # Create example inputs of different sizes.
        meters_input_1 = [
            [0.0, 0.0, 0.0]
        ]
        pixels_input_2 = [
            [0.0, 0.0, 0.0],
            [0.0, 0.0, numpy.pi / 2.0]
        ]
        with patch('os.path.exists') as mock_exist:
            mock_exist.return_value = True
            writer = DataWriter('/output', 'regular', 3, 1, 'c55')
            # Check if images is different.
            with self.assertRaises(ValueError, msg='Different list sizes raises nothing.'):
                writer.write_lists(meters_input_1, pixels_input_2)

    def test_prepare_directory_exist(self) -> None:
        """!
        @brief Ensure that prepare_directory works even if the directory already exists.
        @return None
        """
        with patch('os.path.exists') as mock_exist:
            mock_exist.return_value = True
            with patch('os.makedirs') as mock_make:
                _ = DataWriter('/fake_dir', 'regular', 3, 1, 'c55')
                mock_exist.assert_called_once_with(
                    '/fake_dir/camera_properties')
                mock_make.assert_not_called()

    def test_prepare_directory_not_exist(self) -> None:
        """!
        @brief Ensure that prepare_directory works even if the directory does not exist.
        @return None
        """
        with patch(target='os.path.exists') as mock_exist:
            mock_exist.return_value = False
            with patch('os.makedirs') as mock_make:
                _ = DataWriter('/fake_dir', 'regular', 3, 1, 'c55')
                mock_exist.assert_called_once_with(
                    '/fake_dir/camera_properties')
                mock_make.assert_called_once_with(
                    '/fake_dir/camera_properties')

    def test_prepare_directory_root_exists(self) -> None:
        """!
        @brief Ensure that prepare_directory works if only the root directory exists.
        @return None
        """
        with patch('os.makedirs') as mock_make:
            _ = DataWriter('/opt', 'regular', 3, 1, 'c55')
            mock_make.assert_called_once_with('/opt/camera_properties')

    def test_write_camera_intrinsic_matrix(self) -> None:
        """!
        @brief Tests that the camera intrinsic matrix is correctly written to file.
        @return None
        """
        input_array = numpy.array([
            [1.0, 2.0, 3.0],
            [4.0, -5.25, 6.0],
            [7.0, 8.0, 9.0]
        ])
        camera_name = 'c55'
        expected_file_path = '/opt/camera_properties/c55_intrinsic_matrix.txt'
        expected_output = '1.000000 2.000000 3.000000\n' \
                          '4.000000 -5.250000 6.000000\n' \
            '7.000000 8.000000 9.000000\n'
        with patch(target='os.path.exists') as mock_exist:
            mock_exist.return_value = True
            writer = DataWriter('/opt', 'regular', 3, 1, camera_name)
            with patch(target='builtins.open', new=mock_open()) as mock_output:
                writer.write_camera_intrinsic_matrix(input_array)
                mock_output.assert_called_once_with(
                    file=expected_file_path, mode='w', encoding='utf-8')
                mock_output().write.assert_called_once_with(expected_output)

    def test_write_camera_intrinsic_matrix_wrong_size(self) -> None:
        """!
        @brief Test that the method raises an exception unless a 3x3 matrix is provided.
        @return None
        """
        with patch(target='os.path.exists') as mock_exist:
            mock_exist.return_value = True
            writer = DataWriter('/opt', 'regular', 3, 1, 'c55')
            with self.assertRaises(ValueError,
                                   msg='Write intrinsic matrix does not reject wrong size arrays.'):
                writer.write_camera_intrinsic_matrix(numpy.identity(4))

    def test_write_camera_pose(self) -> None:
        """!
        @brief Test that a camera pose is correctly written to file.
        @return None
        """
        input_array = numpy.array([
            [1.0, 2.0, 3.0, 0.0],
            [4.0, -5.25, 6.0, 0.0],
            [7.0, 8.0, 9.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        camera_name = 'c55'
        expected_file_path = '/opt/camera_properties/c55_pose.txt'
        expected_output = '1.000000 2.000000 3.000000 0.000000\n' \
                          '4.000000 -5.250000 6.000000 0.000000\n' \
                          '7.000000 8.000000 9.000000 0.000000\n' \
                          '0.000000 0.000000 0.000000 1.000000\n'
        with patch(target='os.path.exists') as mock_exist:
            mock_exist.return_value = True
            writer = DataWriter('/opt', 'regular', 3, 1, camera_name)
            with patch(target='builtins.open', new=mock_open()) as mock_output:
                writer.write_camera_pose(input_array)
                mock_output.assert_called_once_with(
                    file=expected_file_path, mode='w', encoding='utf-8')
                mock_output().write.assert_called_once_with(expected_output)

    def test_write_camera_pose_wrong_size(self) -> None:
        """!
        @brief Test that the method raises an exception unless a 4x matrix is provided.
        @return None
        """
        with patch(target='os.path.exists') as mock_exist:
            mock_exist.return_value = True
            writer = DataWriter('/opt', 'regular', 3, 1, 'c55')
            with self.assertRaises(ValueError,
                                   msg='Write intrinsic matrix does not reject wrong size arrays.'):
                writer.write_camera_pose(numpy.identity(3))
