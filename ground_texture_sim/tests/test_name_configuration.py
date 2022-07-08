"""!
@brief This module tests the name_configuration module
"""
import datetime
import unittest
from ground_texture_sim.name_configuration import NameConfigurator


class TestNameConfigurator(unittest.TestCase):
    """!
    @brief Tests the NameConfigurator class.
    """

    def setUp(self) -> None:
        """!
        @brief Create the class and some expected formats for the dates.
        @return None
        """
        ## The class under test
        self._namer = NameConfigurator('/blah/output', 'regular', 3, 2, 'c01')
        current_date = datetime.date.today()
        ## The current date formatted as expected for folder names.
        self._date_folder = current_date.strftime('%y%m%d')
        ## The current date formatted as expected for image names.
        self._date_file = current_date.strftime("%Y-%m-%d")

    def test_create_image_path_absolute(self) -> None:
        """!
        @brief Ensure that create_image_path returns an absolute file path when specified.
        @return None
        """
        image_path = self._namer.create_image_path(5, absolute=True)
        expected_path = F'/blah/output/regular/{self._date_folder}/seq0003/' \
            F'HDG2_t002_regular_{self._date_file}_s0003_c01_i0000005.png'
        self.assertEqual(image_path, expected_path,
                         msg='image_path is not absolute.')

    def test_create_image_path_relative(self) -> None:
        """!
        @brief Ensure that create_image_path returns a relative file path when specified.
        @return None
        """
        image_path = self._namer.create_image_path(5, absolute=False)
        expected_path = F'regular/{self._date_folder}/seq0003/' \
            F'HDG2_t002_regular_{self._date_file}_s0003_c01_i0000005.png'
        self.assertEqual(image_path, expected_path,
                         msg='image_path is not relative.')

    def test_meters_txt_file_correct(self) -> None:
        """!
        @brief Test that the _meters.txt file is named correctly.
        @return None
        """
        expected_path = F'regular_{self._date_folder}_meters.txt'
        self.assertEqual(self._namer.meters_txt_file, expected_path,
                         msg='_meters.txt file not named correctly.')

    def test_test_file_correct(self) -> None:
        """!
        @brief Test that the .test file is named correctly.
        @return None
        """
        expected_path = F'regular_{self._date_folder}.test'
        self.assertEqual(self._namer.test_file, expected_path,
                         msg='.test file not named correctly.')

    def test_txt_file_correct(self) -> None:
        """!
        @brief Test that the .txt file is named correctly.
        @return None
        """
        expected_path = F'regular_{self._date_folder}.txt'
        self.assertEqual(self._namer.txt_file, expected_path,
                         msg='.txt file not named correctly.')
