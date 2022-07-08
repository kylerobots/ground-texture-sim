"""!
@brief This module provides helper functions that transform measurements between coordinate frames
and between type representations.
"""

from typing import List
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
        ## The rotation matrix to transform from image coordinates to camera coordinates.
        self._image_2_camera = numpy.array([
            [0.0, 0.0, 1.0, 0.0],
            [-1.0, 0.0, 0.0, 0.0],
            [0.0, -1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

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

    def project_image_corner(self, robot_pose: numpy.ndarray) -> List[float]:
        """!
        @brief Given a robot's pose in the world, determine what the pose of the top left pixel of
        its image would be in a global image.

        This global image is aligned with the image obtained when the robot is at the origin of the
        world. The pixel value of the corner is found by first projecting it into the robot's frame
        of reference. Then, it is transformed to the origin's frame of reference and projected
        back into this global aligned image.

        @param robot_pose A 4x4 Numpy array containing the homogenous representation of the robot as
        measured from the world frame.
        @return A 3 element list containing the X (in pixels), Y (in pixels), and yaw (in radians)
        of the top left corner of the image.
        """
        # The top left corner is always (0, 0) in pixel space. Add the one for the transform math to
        # work. This will then become the Z component after the scale is applied.
        point_robot_pixel = numpy.array([0.0, 0.0, 1.0]).transpose()
        # Project from pixel space to image coordinates, which are centered in the image with +X to
        # the right of the image and +Y down the image. This normally is only correct to a scale
        # factor of the depth, but we know the depth in this case.
        point_robot_image_truncated = (numpy.linalg.inv(self.camera_intrinsic_matrix) @
                                       point_robot_pixel) * self.camera_pose[2, 3]
        # Now transform to the robot's origin. This requires adding a 1 to be a homogenous
        # representation.
        point_robot_image = numpy.append(point_robot_image_truncated, [1.0], 0)
        point_robot = self.camera_pose @ self._image_2_camera @ point_robot_image
        # Now transform to the origin frame based on the robot's pose
        point_origin = robot_pose @ point_robot
        # Then, transform back into the image frame as if there was a robot aligned at this point.
        point_origin_image = numpy.linalg.inv(
            self.camera_pose @ self._image_2_camera) @ point_origin
        # Normalize to the camera height, then drop the Z component as it is not needed for point
        # projection
        point_origin_image /= self.camera_pose[2, 3]
        point_origin_image_truncated = numpy.array(
            [point_origin_image[0], point_origin_image[1], 1.0]).transpose()
        # Finally, project into the pixel space.
        point_origin_pixel = (self.camera_intrinsic_matrix @
                              point_origin_image_truncated).squeeze()
        # Get the yaw from the robot's original yaw.
        yaw = numpy.arccos(robot_pose[0, 0])
        if numpy.sign(robot_pose[1, 0]) == -1:
            yaw *= -1.0
        return [point_origin_pixel[0], point_origin_pixel[1], yaw]

    def transform_camera_to_world(self, robot_pose: numpy.ndarray) -> numpy.ndarray:
        """!
        @brief Given a robot's pose in the world, determine the pose of the camera in the world.
        @param robot_pose A 4x4 Numpy array containing the homogenous representation of the robot as
        measured from the world frame.
        @return A 4x4 Numpy array representing the pose of the camera as measured from the world
        frame.
        """
        return robot_pose @ self.camera_pose
