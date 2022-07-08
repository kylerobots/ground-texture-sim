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


class TestTransformer(unittest.TestCase):
    """!
    @brief Test the Transformer class works as expected.
    """

    def test_camera_matrix_setter(self) -> None:
        """!
        @brief Test that the getter and setter for camera intrinsic matrix works.
        @return None
        """
        camera_matrix = numpy.array([
            [200.0, 0.0, 500.0],
            [0.0, 200.0, 500.0],
            [0.0, 0.0, 1.0]
        ])
        transformer = transforms.Transformer(numpy.identity(4), camera_matrix)
        self.assertTrue(numpy.allclose(camera_matrix, transformer.camera_intrinsic_matrix),
                        msg='Constructor does not set intrinsic matrix.')
        transformer.camera_intrinsic_matrix = numpy.identity(3)
        self.assertTrue(numpy.allclose(
            numpy.identity(3), transformer.camera_intrinsic_matrix),
            msg='Setter does not set intrinsic matrix.')

    def test_camera_matrix_reject_size(self) -> None:
        """!
        @brief Test that the setter rejects if the wrong size intrinsic matrix is provided.
        @return None
        """
        with self.assertRaises(ValueError,
                               msg='Transformer does not raise exception on bad intrinsic matrix.'):
            transforms.Transformer(numpy.identity(4), numpy.identity(2))
        with self.assertRaises(ValueError,
                               msg='Transformer does not raise exception on bad intrinsic.'):
            transformer = transforms.Transformer(
                numpy.identity(4), numpy.identity(3))
            transformer.camera_intrinsic_matrix = numpy.identity(2)

    def test_camera_pose_setter(self) -> None:
        """!
        @brief Test that the getter and setter for camera pose works.
        @return None
        """
        pose = numpy.array([
            [0.0, 1.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 2.0],
            [0.0, 0.0, 1.0, 3.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        transformer = transforms.Transformer(pose, numpy.identity(3))
        self.assertTrue(numpy.allclose(pose, transformer.camera_pose),
                        msg='Constructor does not set camera pose.')
        transformer.camera_pose = numpy.identity(4)
        self.assertTrue(numpy.allclose(
            numpy.identity(4), transformer.camera_pose), msg='Setter does not set camera pose.')

    def test_camera_pose_reject_size(self) -> None:
        """!
        @brief Test that the setter rejects if the wrong size pose is provided.
        @return None
        """
        with self.assertRaises(ValueError, msg='Transformer does not raise exception on bad pose.'):
            transforms.Transformer(numpy.identity(2), numpy.identity(3))
        with self.assertRaises(ValueError, msg='Transformer does not raise exception on bad pose.'):
            transformer = transforms.Transformer(
                numpy.identity(4), numpy.identity(3))
            transformer.camera_pose = numpy.identity(2)

    def test_project_image_corner_full(self) -> None:
        """!
        @brief Test that the method correctly transforms the corner when at an arbitrary pose.
        @return None
        """
        robot_pose = numpy.array([
            [0.0, -1.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 2.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        camera_pose = numpy.array([
            [0.0, -1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [-1.0, 0.0, 0.0, 0.25],
            [0.0, 0.0, 0.0, 1.0]
        ])
        camera_matrix = numpy.array([
            [2666.666667, 0.000000, 960.000000],
            [0.000000, 2250.000000, 540.000000],
            [0.000000, 0.000000, 1.000000]
        ])
        expected_result = [10986.66666792, -16650.0000001, numpy.pi / 2.0]
        transformer = transforms.Transformer(camera_pose, camera_matrix)
        result = transformer.project_image_corner(robot_pose)
        self.assertEqual(len(expected_result), len(result),
                         msg='Projected point is wrong length.')
        for result_element, expected_element in zip(result, expected_result):
            self.assertAlmostEqual(
                result_element, expected_element, msg='Element of projected point is not correct.')

    def test_project_image_corner_identity(self) -> None:
        """!
        @brief Test that the method correctly transforms the corner when at the origin.
        @return None
        """
        robot_pose = numpy.identity(4)
        camera_pose = numpy.array([
            [0.0, -1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [-1.0, 0.0, 0.0, 0.25],
            [0.0, 0.0, 0.0, 1.0]
        ])
        camera_matrix = numpy.array([
            [2666.666667, 0.000000, 960.000000],
            [0.000000, 2250.000000, 540.000000],
            [0.000000, 0.000000, 1.000000]
        ])
        expected_result = [0.0, 0.0, 0.0]
        transformer = transforms.Transformer(camera_pose, camera_matrix)
        result = transformer.project_image_corner(robot_pose)
        self.assertEqual(len(expected_result), len(result),
                         msg='Projected point is wrong length.')
        for result_element, expected_element in zip(result, expected_result):
            self.assertAlmostEqual(
                result_element, expected_element, msg='Element of projected point is not correct.')

    def test_project_image_corner_negative(self) -> None:
        """!
        @brief Test that the method correctly transforms the corner when the pose has a negative
        yaw.
        @return None
        """
        robot_pose = numpy.array([
            [0.0, 1.0, 0.0, 1.0],
            [-1.0, 0.0, 0.0, 2.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        camera_pose = numpy.array([
            [0.0, -1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [-1.0, 0.0, 0.0, 0.25],
            [0.0, 0.0, 0.0, 1.0]
        ])
        camera_matrix = numpy.array([
            [2666.666667, 0.000000, 960.000000],
            [0.000000, 2250.000000, 540.000000],
            [0.000000, 0.000000, 1.000000]
        ])
        expected_result = [12266.66666808, -18269.9999999, -numpy.pi / 2.0]
        transformer = transforms.Transformer(camera_pose, camera_matrix)
        result = transformer.project_image_corner(robot_pose)
        self.assertEqual(len(expected_result), len(result),
                         msg='Projected point is wrong length.')
        for result_element, expected_element in zip(result, expected_result):
            self.assertAlmostEqual(
                result_element, expected_element, msg='Element of projected point is not correct.')

    def test_transform_camera_to_world_full(self) -> None:
        """!
        @brief Verify that the transform to world function works for some arbitrary values.
        @return None
        """
        robot_pose = numpy.array([
            [-1.0, 0.0, 0.0, 1.0],
            [0.0, -1.0, 0.0, 2.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        camera_pose = numpy.array([
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        expected_result = numpy.array([
            [0.0, 0.0, -1.0, 1.0],
            [0.0, -1.0, 0.0, 2.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        transformer = transforms.Transformer(camera_pose, numpy.identity(3))
        result = transformer.transform_camera_to_world(robot_pose)
        self.assertTrue(numpy.allclose(result, expected_result),
                        msg='Transform math is not correct.')

    def test_transform_camera_to_world_identity(self) -> None:
        """!
        @brief Verify that the transform to world function works when different elements are
        identity.
        @return None
        """
        other_matrix = numpy.array([
            [0.0, 1.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 2.0],
            [0.0, 0.0, 1.0, 3.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        transformer = transforms.Transformer(
            numpy.identity(4), numpy.identity(3))
        # Test when both are identity
        result = transformer.transform_camera_to_world(numpy.identity(4))
        self.assertTrue(numpy.allclose(result, numpy.identity(4)),
                        msg='Transform incorrect for identity.')
        # Test when only one is
        result = transformer.transform_camera_to_world(other_matrix)
        self.assertTrue(numpy.allclose(result, other_matrix),
                        msg='Transform incorrect for identity.')
        transformer.camera_pose = other_matrix
        result = transformer.transform_camera_to_world(numpy.identity(4))
        self.assertTrue(numpy.allclose(result, other_matrix),
                        msg='Transform incorrect for identity.')
