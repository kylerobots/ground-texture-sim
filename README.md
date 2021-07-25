# Ground Texture Simulation #
This package provides an Ignition simulation of realistic ground texture for use by monocular SLAM applications. To
promote fidelity, it uses physics based rendering (PBR) to accurately simulate the appearance of the ground texture.
Additionally, it avoids the repetition of tiles common in most simulated floors.

[Source Code](https://github.com/kylerobots/ground-texture-sim)

[Documentation](https://kylerobots.github.io/ground-texture-sim/)

## License ##
This project is licensed, under the BSD 3-Clause "New" or "Revised" License. See [LICENSE](LICENSE.md) for more info.

It also uses the [Boost tokenizer](https://www.boost.org/doc/libs/1_76_0/libs/tokenizer/doc/index.html) which is subject
to the [Boost license](https://www.boost.org/LICENSE_1_0.txt) and [CPI11](https://github.com/CLIUtils/CLI11) for command
line argument parsing, which is subject to the license shown
[here](https://github.com/CLIUtils/CLI11/blob/master/LICENSE)

## Installation ##
There are three ways to install, depending on your setup. Using the available Docker images is by far the easiest.

### Prebuilt Docker Image ###
There are already built images available at https://hub.docker.com/repository/docker/kylerobots/ground-texture-sim.
Just run the pull command to pull them to your machine.
```bash
docker pull kylerobots/ground-texture-sim:TAG
```
The numbered tags correspond to the release versions described on the GitHub page. The *latest* tag uses the image from
the tip of the *main* branch. This might not be a numbered release, so feature implementation may not be fully
documented.

### Build Your Own Image ###
You can also clone this repository locally and build your own image. You will need git and docker installed on your
computer. When cloning, be sure to use recursive checkout, as this repository uses
[CPI11](https://github.com/CLIUtils/CLI11) as a submodule. Once cloned, you can then build the image.
```bash
git clone --branch VERSION --recursive https://github.com/kylerobots/ground-texture-sim.git
cd ground-texture-sim
docker build --build-arg BUILD_TEST=OFF --target run -t ground-texture-sim:run .
```
In the above example VERSION should be whichever tagged version you wish to use. If you want to build the automated
tests, change BUILD_TEST to ON.

### Compile Source ###
If you wish to install on your computer, you will need a system running Ubuntu 20.04 or 16.04. This is because the
simulation uses Ignition Gazebo, which only works on those OS versions at the moment. Specifically, this has been tested
with Ignition Edifice. You will need the below dependencies. Most are just to support compilation.

* cmake *(installed via apt)*
* gcc *(installed via apt)*
* git *(installed via apt)*
* wget *(installed via apt)*
* ignition edifice *(see [their documentation](https://www.ignitionrobotics.org/docs/edifice/install_ubuntu) for install
instructions)*

After installing the dependencies, run the following commands from wherever you want to put the source code. As this
repository uses submodules, be sure to run recursive
git clone
```bash
git clone --branch VERSION --recursive https://github.com/kylerobots/ground-texture-sim.git
mkdir ground-texture-sim/build
cd ground-texture-sim/build
cmake -DBUILD_TESTING=OFF -DCMAKE_BUILD_TYPE=Release ..
make -j
make install
```
In the above example VERSION should be whichever tagged version you wish to use. If you want to build the automated
tests, change DBUILD_TESTING to ON.

## Running the Code ##
This section describes the various settings used to control the code. There are two nodes that need run - the simulation
and the data collection. Each will be described in order. Then, a convenience launch file that starts both will be
covered. Lastly, this guide provides a quick tip about running everything via Docker.

### Simulation Node ###
The first node in the package is the Ignition simulation itself. This creates a world with realistic ground texture,
realistic lighting, and a downward facing camera for capturing images.
[Ignition's website](https://ignitionrobotics.org/docs) has detailed information about creating these worlds. This
repository also comes with a simple environment. To start that environment, run the following from the repository root.

```bash
ign launch launch/simulate.ign
```
You should see the GUI appear with a camera feed, like so.

![Example GUI](./GUI.png "The Simulation GUI")

The provided launch file starts the simulation and then spawns two models into it; the ground texture model and camera
model. There are launch file parameters that allow specification of other models if you want to provide a different
camera type or ground texture. The way to specify them is as follows:

```bash
ign launch launch/simulate.ign ground:=path/to/ground.sdf camera:=path/to/camera.sdf
```

The values provided for *ground* and *camera* can be absolute or relative paths to a valid SDF file. They can also be a
valid URI for a valid SDF file. The SDF file should contain a single *model* following the
[SDFormat specification](http://sdformat.org/spec?ver=1.8&elem=model). See the examples in *world/ground.sdf* and
*world/camera.sdf* for examples of how these can be formatted.

At this time, changes in lighting require modification of the *world/world.sdf* file. Model spawning uses SDFormat's
*include* tag, which only supports a single model, actor, or light. So there is no way to spawn an arbitrary number of
light sources.

### Trajectory Following ###
The next node does the work of moving the camera around, collecting data, and writing it to file.

#### Inputs ####
There are several parameters that can be customized, but all have default values that work with the code as cloned. This
node takes a number of command line arguments to specify those parameters, or they can be defined in a TOFL formatted
config file. Running the node takes the following forms.
```bash
follow_trajectory --config=path/to/config path/to/trajectory
follow_trajectory --camera_topic=/camera_topic --image_topic=/image_topic ... path/to/trajectory
```
All arguments are optional except for *path/to/trajectory*. An example configuration file and trajectory file are
included in this repository in the *config* subfolder.

The parameters are shown in the following table. You can also run ```follow_trajectory -h``` to view them. They are all
strings except for height, which must be numeric.

| Parameter | Default | Description |
| --- | --- | --- |
| camera_topic | "/camera_info" | The topic publishing camera parameters. |
| height | 0.25 | The height of the camera above the ground. |
| image_topic | "/camera" | The topic publishing the image. |
| move_service | "/world/ground_texture/set_pose" | The service called to move models in simulation. |
| pose_topic | "/world/ground_texture/dynamic_pose/info" | The topic publishing model poses. |
| model | "camera" | The name of the camera model in the simulation. |
| output | "output" |The folder where output data should go. Will be created if it doesn't exist. Can be absolute or relative. |

The trajectory file should be a CSV describing a series of 2D poses for the camera. The path to it can be relative or
absolute. Each line in the file specifies a pose for the camera to collect data from. An example file is included in
the *config* subfolder. The format of the file is like so.
```
x1, y1, yaw1
x2, y2, yaw2
...
xN, yN, yawN
```
Extra values per line will be ignored. If an error occurs on read, the system halts.

#### Examples ####
Here are some quick examples for the different ways to provide inputs.
```bash
# Uses all default values.
follow_trajectory config/trajectory.txt
# Specifies camera height and name via command line and a trajectory file on the desktop.
follow_trajectory --height 0.55 --model camera1 /home/user/Desktop/path.csv
# Specifies parameters via config file and trajectory file both located in a relative folder.
follow_trajectory --config ../specs/config.tofl ../specs/trajectory.txt
```

#### Output ####
As the node runs, it will write data to file. Files will be placed in the location specified by the *output* option
set at runtime. At each pose, it will write three files. One is for the camera pose, one is the image, and one is for
the camera parameters. The format of each named file follows an increasing index as the system moves through poses.

| Data Type | Name Format | Example (For the 3rd pose) |
| --- | --- | --- |
| Image | "%06d.png" | 000002.png |
| Pose | "%06d.txt" | 000002.txt |
| Camera Parameters | "%06d_calib.txt" | 000002_calib.txt |

The image is just a regular PNG file. The pose is a single line text file with the below format. Roll and pitch are
included in case there are slight differences during simulation.
```
x,y,z,roll,pitch,yaw
```
The camera parameters are actually the debug string from the message. While these are unlikely to change at each pose,
they are written to file each time just in case. The file will look like the below.
```
header {
  stamp {
    sec: 132
  }
  data {
    key: "frame_id"
    value: "camera::base_link::camera"
  }
}
width: 1280
height: 960
distortion {
  k: 0
  k: 0
  k: 0
  k: 0
  k: 0
}
intrinsics {
  k: 277
  k: 0
  k: 160
  k: 0
  k: 277
  k: 120
  k: 0
  k: 0
  k: 1
}
projection {
  p: 277
  p: 0
  p: 160
  p: -0
  p: 0
  p: 277
  p: 120
  p: 0
  p: 0
  p: 0
  p: 1
  p: 0
}
rectification_matrix: 1
rectification_matrix: 0
rectification_matrix: 0
rectification_matrix: 0
rectification_matrix: 1
rectification_matrix: 0
rectification_matrix: 0
rectification_matrix: 0
rectification_matrix: 1
```

### Launch File ###
For convenience, there is a launch file that starts both the simulation and data collection. It requires that you
specify a trajectory file. It also allows you to optionally specify a configuration file, ground model, and camera
model. If any of these three are not specified, it will use default values described above. At this time, you cannot
specify other command line options without editing the file itself. An example usage is shown below.
```bash
ign launch launch/generate_data.ign trajectory:=path/to/trajectory config:=path/to/config ground:=path/to/ground.sdf camera:=file:///absolute/path/camera.sdf
```

### Quick Docker Note ###
The above commands can easily be used within the built Docker container. You can also specify them via the CLI with the
Docker run command. This is especially useful if you want to also mount a volume to write data to. As an example,
suppose you have a folder on your Desktop called *data* that already has a configuration file and trajectory file. The
configuration file specifies an *output* value of *data/output*, meaning it will be written in a subfolder.
Additionally, you are using the default camera and ground models. To run the command via Docker, use the below. This
assumes Windows with an X11 server, so the DISPLAY value is set to forward the
GUI.
```powershell
docker run -e DISPLAY=host.docker.internal:0.0 -v "C:\Users\kylerobots\Desktop\data:/home/user/data" ground-texture-sim:run ign launch launch/generate_data.ign config:=data/config.toml trajectory:=data/trajectory.txt
```
You should see the GUI and script output print to the terminal the same as if you were working in your container. After,
you should find that the data has been written to the correct subfolder.

This same concept can be extended to a Docker Compose file, but that is left as an exercise to the reader.

## Extending the Code ##
See the GitHub repository for planned improvements, or to submit your own. You can also use the existing node as a
template to create new ways of inputting the trajectory path. See the CMakeLists.txt file and API for how to use the
*ground_texture_sim* library to do this.