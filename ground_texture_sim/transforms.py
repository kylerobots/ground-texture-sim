"""!
@brief This module provides helper functions that transform measurements between coordinate frames
and between type representations.
"""

import numpy


def create_transform_matrix(x: float, y: float, z: float, roll: float, pitch: float,
                            yaw: float) -> numpy.ndarray:
    """!
    @brief Create a 4x4 homogenous transform matrix from 6 DOF pose information.

    Importantly, the angles are *intrinsic* Euler angles in RPY order.

    @param x The X component of the position, in meters.
    @param y The Y component of the position, in meters.
    @param z The Z component of the position, in meters.
    @param roll The X axis rotation of the orientation, in radians.
    @param pitch The Y axis rotation of the orientation, in radians.
    @param yaw The Z axis rotation of the orientation, in radians.
    @return A 4x4 Numpy array of the homogenous transform matrix for this pose.
    """
    pose = numpy.identity(4)
    pose[0, 3] = x
    pose[1, 3] = y
    pose[2, 3] = z
    rotation_roll = numpy.array([
        [1.0, 0.0, 0.0],
        [0.0, numpy.cos(roll), -numpy.sin(roll)],
        [0.0, numpy.sin(roll), numpy.cos(roll)]
    ])
    rotation_pitch = numpy.array([
        [numpy.cos(pitch), 0.0, numpy.sin(pitch)],
        [0.0, 1.0, 0.0],
        [-numpy.sin(pitch), 0.0, numpy.cos(pitch)]
    ])
    rotation_yaw = numpy.array([
        [numpy.cos(yaw), -numpy.sin(yaw), 0.0],
        [numpy.sin(yaw), numpy.cos(yaw), 0.0],
        [0.0, 0.0, 1.0]
    ])
    pose[0:3, 0:3] = rotation_roll @ rotation_pitch @ rotation_yaw
    return pose


class Transformer:
    """!
    @brief A class to convert poses and points from one frame to another.
    """

    def __init__(self, camera_pose: numpy.ndarray, camera_intrinsic_matrix: numpy.ndarray) -> None:
        """!
        @brief Construct the class with the pose of the camera relative to the robot and camera
        intrinsic matrix.
        @param camera_pose A 4x4 Numpy array that represents the homogenous pose of the camera as
        measured from the robot's frame of reference.
        @param camera_intrinsic_matrix The 3x3 Numpy array that holds the camera's intrinsic matrix.
        """
        ## The camera's pose, as measured from the robot's frame of reference.
        self.camera_pose = camera_pose
        ## The camera intrinsic matrix, generally set in Blender.
        self.camera_intrinsic_matrix = camera_intrinsic_matrix

    @property
    def camera_intrinsic_matrix(self) -> numpy.ndarray:
        """!
        @brief Get the 3x3 camera intrinsic matrix.
        @return A 3x3 Numpy array representing the matrix.
        """
        return self._camera_intrinsic_matrix

    @camera_intrinsic_matrix.setter
    def camera_intrinsic_matrix(self, camera_intrinsic_matrix: numpy.ndarray) -> None:
        """!
        @brief Set the camera intrinsic matrix.
        @param camera_intrinsic_matrix A 3x3 Numpy array representing the matrix.
        @return None
        @exception ValueError if the provided matrix is not 3x3.
        """
        if camera_intrinsic_matrix.shape != (3, 3):
            raise ValueError(
                F'Provided intrinsic matrix should be shape (3, 3), '
                F'not {camera_intrinsic_matrix.shape}.')
        ## The camera intrinsic matrix, generally set in Blender.
        self._camera_intrinsic_matrix = camera_intrinsic_matrix

    @property
    def camera_pose(self) -> numpy.ndarray:
        """!
        @brief Get the 4x4 homogenous pose of the camera as measured from the robot.
        @return A 4x4 Numpy array representing the pose.
        """
        return self._camera_pose

    @camera_pose.setter
    def camera_pose(self, camera_pose: numpy.ndarray) -> None:
        """!
        @brief Set the pose of the camera as measured from the robot's frame of reference.
        @param camera_pose A 4x4 Numpy array containing a homogenous pose.
        @return None
        @exception ValueError if the provided matrix is not 4x4.
        """
        if camera_pose.shape != (4, 4):
            raise ValueError(
                F'Provided intrinsic matrix should be shape (4, 4), not {camera_pose.shape}.')
        ## The camera's pose, as measured from the robot's frame of reference.
        self._camera_pose = camera_pose

    def transform_camera_to_world(self, robot_pose: numpy.ndarray) -> numpy.ndarray:
        """!
        @brief Given a robot's pose in the world, determine the pose of the camera in the world.
        @param robot_pose A 4x4 Numpy array containing the homogenous representation of the robot as
        measured from the world frame.
        @return A 4x4 Numpy array representing the pose of the camera as measured from the world
        frame.
        """
        return robot_pose @ self.camera_pose
