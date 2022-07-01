# Ground Texture Simulation #

![Run Tests](https://github.com/kylerobots/ground-texture-sim/actions/workflows/tests.yml/badge.svg?branch=main)
![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/wiki/kylerobots/ground-texture-sim/python-coverage-comment-action-badge.json)
![Deploy Documentation](https://github.com/kylerobots/ground-texture-sim/actions/workflows/deploy_pages.yml/badge.svg?branch=main)
[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/kylerobots/ground-texture-sim)

## Table of Contents ##
1. [License](#license)
2. [Install](#install)
    1. [Local Blender](#blender-installed-locally)
    2. [Local Container](#build-container-locally)
    3. [Prebuilt Container](#pull-docker-hub-container)
3. [Running](#running)
4. [Customization](#customization)
    1. [Customizing the Output](#customizing-the-output)
    2. [Customizing the Environment](#customizing-the-environment)


This package helps create realistic ground texture synthetic images for use by a monocular SLAM application. To promote
fidelity, it uses physics based rendering (PBR) to accurately simulate the appearance of the ground texture.
Additionally, it avoids the repetition of tiles common in most simulated floors.

[Source Code](https://github.com/kylerobots/ground-texture-sim)

[Documentation](https://kylerobots.github.io/ground-texture-sim/)

## License ##
Copyright 2022 Kyle M. Hart

See [LICENSE](LICENSE.md) for more info.

Since v3.0.0 and on relies on Blender's API, it is licensed under GPLv3 and later. There is no code reuse between
v3.0.0 and previous versions, so no conflict with previous licenses.

The example texture provided in this repository comes from [Poly Haven](https://polyhaven.com/a/t_brick_floor_002) and
is licensed under [CC0](https://creativecommons.org/publicdomain/zero/1.0/)

The format for the data comes from this repository: https://github.com/JanFabianSchmid/HD_Ground and is licensed under
CC BY-SA: 4.0

## Install ##
There are three ways to use this, depending on your preferred setup. Regardless of the setup, make sure your PYTHONPATH
environmental variable contains the directory of this code so that Blender can find all of the scripts.

### Blender Installed Locally ###
If you already have Blender installed locally, you only need to clone the repository to your computer:

```bash
git clone --branch VERSION https://github.com/kylerobots/ground-texture-sim.git
```

### Build Container Locally ###
If you don't have Blender, this code also provides a Dockerfile that will create an image with Blender. Just
run the following:

```bash
git clone --branch VERSION https://github.com/kylerobots/ground-texture-sim.git
cd ground-texture-sim
docker build --target run -t ground-texture-sim:run .
```

The resulting image will have Blender, the generation scripts, and the example environment. If you are only
interacting with the environment via the configuration file, you don't need to get the GUI working. Any other
features and you do.

### Pull Docker Hub Container ###
If you don't want to build anything yourself, you can just pull a prebuilt container from Docker Hub:
```bash
docker pull kylerobots/ground-texture-sim:TAG
```
Make sure the tag is at least `3.0.0`

## Running ##
To run the script, enter the following from the command line in the root directory of the project, This example
generates data for the example provided in example_setup.

```bash
blender example_setup/environment.blend -b --python generate_data.py --python-use-system-env -- config.json
```

You can substitute `example_setup/environment.blend` for another Blender environment you may have. Likewise,
`config.json` should be replaced with the name of the configuration JSON file that specifies everything for your
project. An example JSON file can be found at the root directory of this project.

The `-b` flag will run Blender in the background, so you don't need to open it up. However, you may use Blender as
usual to adjust lighting, the scene, or anything else not currently supported by this script.

The `--python-use-system-env` flag allows Blender to search for modules on your PYTHONPATH instead of just within
Blender's instance of Python. This is essential for all the necessary code to run.

The data is output to the location specified by `output` in the JSON. There are multiple files and folders. At the top
level are three list files. The one ending in `.test` lists a relative path to each image in the sequence. The ones that
end in `.txt` both contain lists alternating between the relative path to each image and a global pose, stored as a 3x3
homogenous matrix. The difference between the two is that the one with a `_meters.txt` suffix stores the global pose of
a simulated robot carrying the camera. The one with just `.txt` notes the pose of the top left pixel of the image, in
pixel space. In other words, the origin of this space is the origin of the top left corner of the image taken when the
simulated robot is at (0, 0, 0).

Additionally there are two folders. The first, called `camera_properties` contains text files with the camera intrinsic
matrix, called `<camera_name>_intrinsic_matrix.txt`, and the camera's pose as measured from the simulated robot, called
`<camera_name>_pose.txt`. The next folder is a series of nested folders containing the images. The names of the folders
and image files are based on the values set in the JSON and have the format:
`<sequence_type>/<date>/<sequence_number>/HDG2_t<texture_number>_<sequence_type>_<date>_<sequence_number>_<camera_name>_i#######.png`
This comes from the format specified here: https://github.com/JanFabianSchmid/HD_Ground

Note that, depending on your settings and computing power, this script may take some time to execute. The script will
continually provide progress updates as it goes.

## Customization ##

### Customizing the Output ###
The below example JSON and table show what values can currently be specified in the configuration JSON. The table also
lists if a parameter is required and its default if not required.

```json
{
  "trajectory": "example_setup/trajectories/corners_1x1.txt",
  "output": "output",
  "sequence": {
    "texture_number": 1,
    "sequence_type": "regular",
    "sequence_number": 1
  },
  "camera": {
    "name": "Camera",
    "x": 0.0,
    "y": 0.0,
    "z": 0.25,
    "roll": 0.0,
    "pitch": 1.5708,
    "yaw": 0.0
  }
}
```

| Parameter Key | Required? | Default Value | Description |
| ------------- | :-------: | :-----------: | ----------- |
| trajectory    | Yes       | *N/A*         | The name of the file to read the list of poses the robot should take. Each line in the file should be of the form `x, y, yaw (radians)` |
| output        | Yes       | *N/A*         | The folder the images and calibration file should be written to. Can be absolute or relative |
| sequence/texture_number | Yes | *N/A* | An integer designation of the texture used in this sequence |
| sequence/sequence_type | Yes | *N/A* | A string describing what type of sequence, such as "regular" or "lawnmower" |
| sequence/sequence_number | Yes | *N/A* | A unique integer relative to this particular texture and date of data collection |
| camera/name | Yes | *N/A* | The name in Blender for the camera. |
| camera/x | No | 0.0 | The X component of the translation of the camera from the simulated robot's frame. |
| camera/y | No | 0.0 | The Y component of the translation of the camera from the simulated robot's frame. |
| camera/z | No | 0.0 | The Z component of the translation of the camera from the simulated robot's frame. |
| camera/roll | No | 0.0 | The roll of the orientation, in RPY Euler angles and radians, of the camera from the simulated robot's frame |
| camera/pitch | No | 1.5708 | The pitch of the orientation, in RPY Euler angles and radians, of the camera from the simulated robot's frame |
| camera/yaw | No | 0.0 | The yaw of the orientation, in RPY Euler angles and radians, of the camera from the simulated robot's frame |

Note that while any 6 DOF pose of the camera is technically possible, deviations too far from a downward facing camera
are unspecified. It also represents the pose of the camera relative to each trajectory pose. In other words, if the
trajectories specified in the trajectory file are a robot's origin on the ground plane, these values are the pose of the
camera with respect to the robot's origin. This is provided to allow easy data generation of cases where the camera may
be misaligned or off-center. Importantly, the roll, pitch, and yaw are Euler angles applied in that order and are
*extrinsic* rotations. The values are in meters and radians. Additionally, values of zero on all six dimensions will
align the camera image with the robot's frame of reference, so it won't be pointed at the ground. You will typically
want a pitch of pi / 2.0 or close to that for a downward facing camera. While this is counterintuitive for this
application, this adheres to frame conventions in the greater robotics community.

### Customizing the Environment ###
For any other setting, such as different textures or image size, you will need to open up Blender and edit the .blend
file. This is due to the extremely large number of settings that are possible. Consequently, this guide will not
cover them all. However, here are some common items to consider. This assumes basic familiarity with Blender.

* The device used for rendering can be selected on the `render properties` pane, under `Device`. It is encouraged to use
the GPU if available.
* The quality of the render can be changed by adjusted the `Render > Samples` setting on the `render properties` pane.
The higher the number, the higher quality the image (and longer render time).
* The size of the output image is found in the `Output Properties` pane, under `Format`.
* To change the ground texture, navigate to the `Shading` workspace and select the `Ground` object in the Scene
Collection. You will see a bunch of nodes connected together. The four brown ones are the PBR files. Each one is named
for the type of file it should hold (e.g. `normal` for the `normal` file). Use the file browser on each node to change
to a new texture.
* The size of the ground can be changed by selecting `Ground` in the Scene Collection, then navigating to the
`Object Properties` pane. Use the X and Y scale. The example file has a ground that is 2x2 meters. The texture will
stretch to fit whatever the ground size is.
* The camera parameters are not set as a matrix, but rather as a combination of the image resolution and properties
specified in the `Object Data Properties` pane found when selecting the `Camera` from the Scene Collection. See
https://visp-doc.inria.fr/doxygen/visp-3.4.0/tutorial-tracking-mb-generic-rgbd-Blender.html for a good overview of how
these parameters impact the intrinsic matrix.