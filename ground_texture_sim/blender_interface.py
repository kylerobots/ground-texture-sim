"""!
@brief This module provides the necessary functions to interact with Blender.
"""
from os import path
from math import pi
import bpy
import mathutils
import numpy


class BlenderInterface():
    """!
    @brief This class interfaces with Blender to set and get various properties.
    """

    def __init__(self, camera_name: str = 'Camera') -> None:
        """!
        @brief Create the interface with the specified name for the camera in Blender.
        @param camera_name The name of the camera in the target Blender environment. Defaults to
        "Camera".
        """
        ## The name of the selected camera in the Blender interface.
        self.camera_name = camera_name

    @property
    def camera_intrinsic_matrix(self) -> numpy.ndarray:
        """!
        @brief Get the 3x3 intrinsic matrix from the target Blender environment.

        This is a 3x3 matrix derived from Blender using these steps:
        https://visp-doc.inria.fr/doxygen/visp-3.4.0/tutorial-tracking-mb-generic-rgbd-Blender.html

        @return A 3x3 numpy array representing the intrinsic matrix.
        """
        camera = bpy.data.objects[self.camera_name]
        focal_length = camera.data.lens
        scene = bpy.context.scene
        resolution_x_px = scene.render.resolution_x
        resolution_y_px = scene.render.resolution_y
        scale = scene.render.resolution_percentage / 100.0
        sensor_width_mm = camera.data.sensor_width
        sensor_height_mm = camera.data.sensor_height
        aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
        if camera.data.sensor_fit == 'VERTICAL':
            s_u = resolution_x_px * scale / sensor_width_mm / aspect_ratio
            s_v = resolution_y_px * scale / sensor_height_mm
        else:
            aspect_ratio = scene.render.pixel_aspect_x / scene.render.pixel_aspect_y
            s_u = resolution_x_px * scale / sensor_width_mm
            s_v = resolution_y_px * scale * aspect_ratio / sensor_height_mm
        alpha_u = focal_length * s_u
        alpha_v = focal_length * s_v
        u_0 = resolution_x_px * scale / 2
        v_0 = resolution_y_px * scale / 2
        skew = 0
        matrix = numpy.array([
            [alpha_u, skew, u_0],
            [0.0, alpha_v, v_0],
            [0.0, 0.0, 1.0]
        ])
        return matrix

    @property
    def camera_name(self) -> str:
        """!
        @brief Gets the name of the camera in Blender.
        @return A string of the camera name to use when interacting with Blender.
        """
        return self._camera_name

    @camera_name.setter
    def camera_name(self, camera_name: str) -> None:
        """!
        @brief Sets the name of the camera in Blender.
        @param camera_name The name of the camera to control in the target Blender environment.
        @return None
        @exception NameError if the provided camera name is not found in the target Blender
        environment.
        """
        if camera_name not in bpy.data.cameras.keys():
            raise NameError(
                F'{camera_name} is not a Blender camera. Available cameras '
                F'are: {bpy.data.cameras.keys()}'
            )
        ## The name of the selected camera in the Blender interface.
        self._camera_name = camera_name

    def generate_image(self, image_path: str, x: float, y: float, z: float, roll: float,
                       pitch: float, yaw: float) -> None:
        """!
        @brief Position the camera at a designated pose and render an image.

        This method takes the 6 DOF pose of the camera, places the camera at that pose in the
        environment, renders the image, then saves the image to the designated file.

        The 6 arguments specifying the pose are the pose of the camera in the world frame. The roll,
        pitch, and yaw are Euler angles in radians and are specified as *extrinsic* rotations in
        roll, pitch, yaw order.

        Blender's coordinate system is different than the usual coordinate system assumed in
        robotics. This method adds the correct adjustment, so there is no need to account for it.

        @param image_path An absolute path to where the image should go. Blender does not seem to
        handle relative paths great.
        @param x The X component of the translation, in meters, of the camera in the world's frame.
        @param y The Y component of the translation, in meters, of the camera in the world's frame.
        @param z The Z component of the translation, in meters, of the camera in the world's frame.
        @param roll The X axis component of the rotation, in radians, of the camera in the world's
        frame. The rotation is performed as *extrinsic* RPY Euler angles.
        @param pitch The Y axis component of the rotation, in radians, of the camera in the world's
        frame. The rotation is performed as *extrinsic* RPY Euler angles.
        @param yaw The Z axis component of the rotation, in radians, of the camera in the world's
        frame. The rotation is performed as *extrinsic* RPY Euler angles.
        @return None
        @exception ValueError raised if the provided path is not absolute.
        """
        # Verify the path is absolute.
        if not path.isabs(image_path):
            raise ValueError(
                F'Image path must be absolute. Received: {image_path}')
        # Convert the provided pose into a transform matrix.
        pose_translation = mathutils.Matrix.Translation(vector=(x, y, z))
        pose_rotation = mathutils.Euler(
            angles=(roll, pitch, yaw), order='XYZ').to_matrix().to_4x4()
        pose = pose_translation @ pose_rotation
        # Calculate the offset to get Blender to position the camera correctly.
        # Pre-compute the offset used to get blender camera poses correct.
        blender_adjustment = mathutils.Euler(
            angles=(pi/2.0, 0.0, -pi/2.0), order='XYZ').to_matrix().to_4x4()
        blender_placement = pose @ blender_adjustment
        # Now place the camera
        camera = bpy.data.cameras[self.camera_name]
        camera.location.x = blender_placement.to_translation()[0]
        camera.location.y = blender_placement.to_translation()[1]
        camera.location.z = blender_placement.to_translation()[2]
        camera.rotation_euler.x = blender_placement.to_euler('XYZ')[0]
        camera.rotation_euler.y = blender_placement.to_euler('XYZ')[1]
        camera.rotation_euler.z = blender_placement.to_euler('XYZ')[2]
        # Render the image
        bpy.context.scene.render.filepath = image_path
        bpy.ops.render.render(write_still=True)
