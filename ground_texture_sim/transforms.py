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
