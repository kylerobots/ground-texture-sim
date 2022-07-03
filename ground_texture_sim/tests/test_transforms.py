"""!
@brief This module tests the transforms module.
"""
import unittest
import numpy
from ground_texture_sim import transforms


class TestCreateTransformMatrix(unittest.TestCase):
    """!
    @brief Test that the create_transform_matrix function works.
    """

    def test_full_rotation(self) -> None:
        """!
        @brief Test the function works with arbitrary values.
        @return None
        """
        expected_result = numpy.array([
            [0.0, 0.0, 1.0, 1.0],
            [1.0, 0.0, 0.0, 2.0],
            [0.0, 1.0, 0.0, 3.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        result = transforms.create_transform_matrix(
            1.0, 2.0, 3.0, numpy.pi, numpy.pi / 2.0, -numpy.pi / 2.0)
        self.assertTrue(numpy.allclose(expected_result, result))

    def test_identity(self) -> None:
        """!
        @brief Test that zeros produce the identity transform.
        @return None
        """
        expected_result = numpy.identity(4)
        result = transforms.create_transform_matrix(
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.assertTrue(numpy.allclose(expected_result, result))
