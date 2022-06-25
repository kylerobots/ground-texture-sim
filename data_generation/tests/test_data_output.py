"""!
This module tests the data_output module.
"""
import datetime
import unittest
from math import pi
from unittest.mock import mock_open, patch
from typing import Dict, List, Tuple
from data_generation import data_output


class TestPrepareOutputFolder(unittest.TestCase):
    """!
    This class verifies that the prepare_output_folder function works.
    """

    def test_exists(self) -> None:
        """!
        This verifies nothing happens if the folders already exist.

        @return None
        """
        with patch('os.path.exists') as mock_exist:
            mock_exist.return_value = True
            with patch('os.makedirs') as mock_make:
                data_output.prepare_output_folder('/fake_dir')
                mock_exist.assert_called_once_with(
                    '/fake_dir/camera_properties')
                mock_make.assert_not_called()

    def test_not_exist(self) -> None:
        """!
        This method verifies the directory is created if neither the output nor subdirectory exists.

        @return None
        """
        with patch(target='os.makedirs') as mock:
            data_output.prepare_output_folder('/fake_dir')
            mock.assert_called_once_with('/fake_dir/camera_properties')

    def test_root_exists(self) -> None:
        """!
        This method verifies the subfolder directory is created if it doesn't exist.

        @return None
        """
        with patch(target='os.makedirs') as mock:
            data_output.prepare_output_folder('/opt/')
            mock.assert_called_once_with('/opt/camera_properties')


class TestWriteCameraIntrinsicMatrix(unittest.TestCase):
    """!
    This class verifies that the function to write the intrinsic matrix works.
    """

    def test_name_not_found(self) -> None:
        """!
        Verifies an error is raised if the camera name is bad.

        @return None
        """
        with patch(target='data_generation.blender_interface.get_camera_intrinsic_matrix') as mock:
            mock.side_effect = Exception('Cannot find camera')
            with self.assertRaises(NameError, msg='Does not raise error on incorrect name'):
                data_output.write_camera_intrinsic_matrix(
                    'fake_name', 'output')

    def test_success(self) -> None:
        """!
        Verifies the matrix is written correctly if everything is good.

        @return None
        """
        expected_output = '0.000000 1.000000 2.000000\n' \
            '3.000000 4.000000 5.000000\n' \
            '6.000000 7.000000 8.000000\n'
        with patch('data_generation.blender_interface.get_camera_intrinsic_matrix') as mock_blender:
            mock_blender.return_value = [
                0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
            with patch(target='builtins.open', new=mock_open()) as mock_output:
                data_output.write_camera_intrinsic_matrix(
                    'camera', 'output_folder')
                mock_output().write.assert_called_once_with(expected_output)


class TestWriteCameraPose(unittest.TestCase):
    """!
    This class verifies that the camera pose is written as a homogenous matrix to file.
    """

    def test_identity(self) -> None:
        """!
        This method verifies the correct identity matrix is written.

        @return None
        """
        camera_properties = {
            'name': 'camera',
            'x': 0.0,
            'y': 0.0,
            'z': 0.0,
            'roll': 0.0,
            'pitch': 0.0,
            'yaw': 0.0
        }
        expected_output = '1.000000 0.000000 0.000000 0.000000\n' \
            '0.000000 1.000000 0.000000 0.000000\n' \
            '-0.000000 0.000000 1.000000 0.000000\n' \
            '0.000000 0.000000 0.000000 1.000000\n'
        with patch(target='builtins.open', new=mock_open()) as mock:
            data_output.write_camera_pose(camera_properties, '/output_folder')
            mock.assert_called_once_with(
                file='/output_folder/camera_properties/camera_pose.txt', mode='w', encoding='utf8')
            mock().write.assert_called_once_with(expected_output)

    def test_example(self) -> None:
        """!
        This method verifies the output correctly assembles a homogenous
        transform.

        @return None
        """
        camera_properties = {
            'name': 'c15',
            'x': 1.0,
            'y': 2.0,
            'z': 3.0,
            'roll': pi / 2.0,
            'pitch': -pi / 2.0,
            'yaw': pi
        }
        expected_output = '-0.000000 1.000000 0.000000 1.000000\n' \
            '0.000000 -0.000000 1.000000 2.000000\n' \
            '1.000000 0.000000 0.000000 3.000000\n' \
            '0.000000 0.000000 0.000000 1.000000\n'
        with patch(target='builtins.open', new=mock_open()) as mock:
            data_output.write_camera_pose(camera_properties, 'output_folder')
            mock.assert_called_once_with(
                file='output_folder/camera_properties/c15_pose.txt', mode='w', encoding='utf8')
            mock().write.assert_called_once_with(expected_output)


class TestWriteListFiles(unittest.TestCase):
    """!
    This class verifies that the list files are written correctly.
    """

    def _create_inputs(self) -> Tuple[Dict, List[List[float]]]:
        """!
        Convenience function to create the inputs to the write_list_files function.

        @return A tuple containing the configs Dict and trajectory List
        """
        configs = {
            'camera': {
                'name': 'c01'
            },
            'output': '/opt/output',
            'sequence': {
                'sequence_type': 'test1',
                'sequence_number': 1,
                'texture_number': 245
            }
        }
        trajectory = [
            [0.0, 0.0, 0.0],
            [1.2, 3.5, pi / 2.0]
        ]
        return configs, trajectory

    def test_success_absolute(self) -> None:
        """!
        Test the function writes correctly with an absolute output path.

        @return None
        """
        configs, trajectory = self._create_inputs()
        current_date = datetime.date.today()
        date_string = current_date.strftime('%y%m%d')
        image_string = current_date.strftime('%Y-%m-%d')
        # Create the expected lines that will be written.
        image_strings = [
            F'test1/{date_string}/seq0001/HDG2_t245_test1_{image_string}_s0001_c01_i0000000.png\n',
            F'test1/{date_string}/seq0001/HDG2_t245_test1_{image_string}_s0001_c01_i0000001.png\n'
        ]
        ground_truth_strings = [
            '1.000000 -0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000\n',
            '0.000000 -1.000000 1.200000 1.000000 0.000000 3.500000 0.000000 0.000000 1.000000\n'
        ]
        pixel_strings = [
            ' \n',
            ' \n'
        ]
        with patch(target='builtins.open', new=mock_open()) as mock:
            data_output.write_list_files(configs, trajectory)
            # Verify the correct files are written to
            mock.assert_any_call(
                file=F'/opt/output/test1_{date_string}.test', mode='w', encoding='utf-8')
            mock.assert_any_call(
                file=F'/opt/output/test1_{date_string}.txt', mode='w', encoding='utf-8')
            mock.assert_any_call(
                file=F'/opt/output/test1_{date_string}_meters.txt', mode='w', encoding='utf-8')
            # Verify the right information is written. This won't verify the order though or that
            # each one is in the correct file. Just the formatting.
            mock().write.assert_any_call(image_strings[0])
            mock().write.assert_any_call(image_strings[1])
            mock().write.assert_any_call(ground_truth_strings[0])
            mock().write.assert_any_call(ground_truth_strings[1])
            mock().write.assert_any_call(pixel_strings[0])
            mock().write.assert_any_call(pixel_strings[1])

    def test_success_relative(self) -> None:
        """!
        Test the function writes correctly with a relative output path.

        This doesn't need to check the actual file contents, as that will be covered by
        @ref test_success_absolute

        @return None
        """
        configs, trajectory = self._create_inputs()
        configs['output'] = 'output'
        current_date = datetime.date.today()
        date_string = current_date.strftime('%y%m%d')
        with patch(target='builtins.open', new=mock_open()) as mock:
            data_output.write_list_files(configs, trajectory)
            # Verify the correct files are written to
            mock.assert_any_call(
                file=F'output/test1_{date_string}.test', mode='w', encoding='utf-8')
            mock.assert_any_call(
                file=F'output/test1_{date_string}.txt', mode='w', encoding='utf-8')
            mock.assert_any_call(
                file=F'output/test1_{date_string}_meters.txt', mode='w', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
