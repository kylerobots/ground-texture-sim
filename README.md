# Ground Texture Simulation #

![Run Tests](https://github.com/kylerobots/ground-texture-sim/actions/workflows/tests.yml/badge.svg?branch=main)
![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/wiki/kylerobots/ground-texture-sim/python-coverage-comment-action-badge.json)
![Deploy Documentation](https://github.com/kylerobots/ground-texture-sim/actions/workflows/deploy_pages.yml/badge.svg?branch=main)
[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/kylerobots/ground-texture-sim)

This package helps create realistic ground texture synthetic images for use by a monocular SLAM application. To promote
fidelity, it uses physics based rendering (PBR) to accurately simulate the appearance of the ground texture.
Additionally, it avoids the repetition of tiles common in most simulated floors.

[Source Code](https://github.com/kylerobots/ground-texture-sim)

[Documentation](https://kylerobots.github.io/ground-texture-sim/)

## License ##
Copyright 2022 Kyle M. Hart

See [LICENSE](LICENSE.md) for more info.

Since v3.0.0 and on relies on Blender's API, it is licensed under GPLv3 and later. There is not code reuse between
v3.0.0 and previous versions, so no conflict with previous licenses.

The example texture provided in this repository comes from [Poly Haven](https://polyhaven.com/a/t_brick_floor_002) and
is licensed under [CC0](https://creativecommons.org/publicdomain/zero/1.0/)

## Install ##
There are three ways to use this, depending on your preferred setup.

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
To run the script, enter the following from the command line in the root directory of the project:

```bash
blender environment.blend -b --python data_generation.py -- config.json
```

You can substitute `environment.blend` for another environment you may have. Likewise, `config.json` should be replaced
with the name of the configuration JSON file that specifies everything for your project. An example file can be found
at the root directory of this project.

The `-b` flag will run Blender in the background, so you don't need to open it up. However, you may use Blender as
usual to adjust lighting, the scene, or anything else not currently supported by this script. The images will write to
the specified folder, as shown below. A file called `calibration.txt` will also be written. It contains the camera
intrinsic matrix for this simulation run.

Note that, depending on your settings and computing power, this script may take some time to execute. The script will
continually provide progress updates as it goes.

### Customizing the Run ###
All settings can be specified in the configuration JSON file. The allowed values are as follows:

| Parameter Key | Required? | Default Value | Description |
| ------------- | :-------: | :-----------: | ----------- |
| camera height | Yes       | *N/A*         | The height, in meters the camera is above the ground plane. |
| output        | Yes       | *N/A*         | The folder the images and calibration file should be written to. Can be absolute or relative |
| trajectory    | Yes       | *N/A*         | The name of the file to read the list of poses. Each line in the file should be of the form: `x, y, yaw` |
