"""!
This module provides the necessary functions to interact with Blender.
"""
from typing import Dict, List
from math import pi
from os import path
import datetime
import bpy
import mathutils


def _create_image_path(index: int, configs: Dict) -> str:
    """!
    Assemble the directory and name of the particular image to use for the filename.

    From the output directory, this will go in:
    ```
    sequence_type/date_collected/sequence_number/
    HDG$VersionNumber_t$TextureNumber_$SequenceType_
    $DateOfRecording_s$SequenceNumber_c01_i$ImageNumber.png
    ```

    @param index The image number to use
    @param configs The well-formatted Dict containing the necessary sequence settings
    @return An absolute path to the image location.
    """
    current_date = datetime.date.today()
    # First, assemble the directory
    sequence_type_folder = configs['sequence']['sequence_type']
    date_folder = current_date.strftime('%y%m%d')
    sequence_number_folder = F'seq{configs["sequence"]["sequence_number"]:03d}'
    file_directory = path.join(
        configs['output'], sequence_type_folder, date_folder, sequence_number_folder)
    # Then the filename
    texture_name = F't{configs["sequence"]["texture_number"]:03d}'
    sequence_type_name = F'{configs["sequence"]["sequence_type"]}'
    date_name = current_date.strftime('%Y-%m-%d')
    sequence_number_name = F's{configs["sequence"]["sequence_number"]:04d}'
    camera_name = F'{configs["camera"]["name"]}'
    image_name = F'i{index:07d}'
    file_name = F'HDG2_{texture_name}_{sequence_type_name}_{date_name}' \
        F'_{sequence_number_name}_{camera_name}_{image_name}.png'
    full_path = path.abspath(path.join(file_directory, file_name))
    return full_path


def generate_images(configs: Dict, trajectory: List[List[float]]) -> None:
    """!
    Generate an image at each trajectory point via Blender's interface.

    This iterates through each pose in the trajectory, moves the camera to the correct spot, then
    renders the image.

    @param configs The configuration values specified in the JSON file.
    @param trajectory A list of poses, of the form [x, y, theta].
    @return None
    """
    camera = bpy.data.objects[configs['camera']['name']]
    # Calculate the trajectory to camera transform from the provided parameters.
    trajectory_2_camera_translation = mathutils.Matrix.Translation(
        (configs['camera']['x'], configs['camera']['y'], configs['camera']['z']))
    trajectory_2_camera_rotation = mathutils.Euler((configs['camera']['roll'],
                                                    configs['camera']['pitch'],
                                                    configs['camera']['yaw']),
                                                   'XYZ').to_matrix().to_4x4()
    trajectory_2_camera = trajectory_2_camera_translation @ trajectory_2_camera_rotation
    # Blender's origin pose is pointing straight down. While this may seem beneficial, it is
    # inconsistent with robot frame conventions, so apply a correcting factor that, if
    # trajectory_2_camera is identity, aligns the camera with the trajectory/robot pose.
    blender_adjustment = mathutils.Euler(
        (pi/2.0, 0.0, -pi/2.0), 'XYZ').to_matrix().to_4x4()
    trajectory_2_camera = trajectory_2_camera @ blender_adjustment
    # Iterate through each pose in the trajectory
    for i, pose in enumerate(trajectory):
        # Figure out the camera's global pose by combining this pose with the one computed above.
        trajectory_pose_rotation = mathutils.Matrix.Rotation(pose[2], 4, 'Z')
        trajectory_pose_translation = mathutils.Matrix.Translation(
            (pose[0], pose[1], 0.0))
        trajectory_pose = trajectory_pose_translation @ trajectory_pose_rotation
        # Combine them to get the camera's pose
        camera_pose = trajectory_pose @ trajectory_2_camera
        # Use this to position in Blender
        camera.location.x = camera_pose.to_translation()[0]
        camera.location.y = camera_pose.to_translation()[1]
        camera.location.z = camera_pose.to_translation()[2]
        camera.rotation_euler.x = camera_pose.to_euler('XYZ')[0]
        camera.rotation_euler.y = camera_pose.to_euler('XYZ')[1]
        camera.rotation_euler.z = camera_pose.to_euler('XYZ')[2]
        # Render the image into the output directory
        bpy.context.scene.render.filepath = _create_image_path(i, configs)
        bpy.ops.render.render(write_still=True)


def get_camera_intrinsic_matrix(camera_name: str) -> List[float]:
    """!
    Calculate the intrinsic calibration matrix of Blender's camera.

    This is a 3x3 matrix derived from Blender using these steps:
    https://visp-doc.inria.fr/doxygen/visp-3.4.0/tutorial-tracking-mb-generic-rgbd-Blender.html

    @param camera_name The name of the camera in Blender.
    @return A 9 element list representing the 3x3, row major intrinsic matrix.
    """
    camera = bpy.data.objects[camera_name]
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
    matrix = [alpha_u, skew, u_0, 0.0, alpha_v, v_0, 0.0, 0.0, 1.0]
    return matrix
