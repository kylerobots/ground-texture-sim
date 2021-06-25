# Ground Texture Simulation
This package provides an Ignition simulation of realistic ground texture for use by monocular SLAM applications. To
promote fidelity, it uses physics based rendering (PBR) to accurately simulate the appearance of the ground texture.
Additionally, it avoids the repetition of tiles common in most simulated floors.

[Source Code](https://github.com/kylerobots/ground-texture-sim)

[Documentation](https://kylerobots.github.io/ground-texture-sim/)

## Installing ##
There are two ways to use this. The code comes with a Dockerfile. If you build that, it has all the dependencies that
you need. The *run* stage is a minimal version that has the commands needed to run. Build it with:
```powershell
docker build --target run -t ground-texture-sim:run .
```
There is also fully compiled images available at https://hub.docker.com/repository/docker/kylerobots/ground-texture-sim
that can be pulled and used immediately.

Alternatively, you can use this directly on your computer. As of now, it only supports Ubuntu Bionic or Focal.
This is because the simulation uses Ignition Gazebo, which only works on those OS versions at the moment. Specifically,
this has been tested with Ignition Edifice. You will need the below dependencies. Most are just to support compilation.

* cmake *(installed via apt)*
* build-essential *(installed via apt)*
* git *(installed via apt)*
* wget *(installed via apt)*
* ignition edifice *(see [their documentation](https://www.ignitionrobotics.org/docs/edifice/install_ubuntu) for install
instructions)*

After installing the dependencies, run the following commands from wherever you want to put the source code.
```bash
git clone https://github.com/kylerobots/ground-texture-sim.git
mkdir ground-texture-sim/build
cd ground-texture-sim/build
cmake ..
make -j
```

## Running ##
The preferred way to run the simulation is with the included launch file. It starts the simulation, keyboard control,
and data writing in one go. The command, if running from the root directory is 
```bash
ign launch launch/keyboard.ign
```
It is also the default command for the Dockerfile, so can be run that way.
```powershell
docker run -e DISPLAY=host.docker.internal:0.0 ground-texture-sim:run
```
In that example, it assumes running on a Windows host (so setting the right DISPLAY variable) and that the image is
tagged according to the previous build instructions.

If you wish to start each part individually, instructions are below. They can be run in the Docker containers or on
your computer, depending on how you installed everything.

### Simulation ###
To start the Gazebo simulation, run this from the root level of the code:
```bash
ign gazebo world/world.sdf
```
You should see the GUI appear with a camera feed, like so.
![Example GUI](GUI.png)

### Keyboard Controller ###
To start the keyboard control of the camera, run this from the build directory:
```bash
./keyboard_controller
```
There won't be anything printed on the terminal. You can then go to the GUI and press any of the keys listed on the
table to get the corresponding velocities. A key press will set the listed velocity for 0.5 seconds. After which, it
will return to 0 if no other key has been pressed. You can also hold a key down to maintain the given velocity. You
can also press multiple keys in succession to get a more complex velocity. However, holding multiple keys is
unsupported (by the keyboards, not this software).

| Key | X (m/s) | Y (m/s) | Theta (rad/s) |
| --- | ------- | ------- | ------------- |
| A   | 0.0     | -0.5    | 0.0           |
| S   | -0.5    | 0.0     | 0.0           |
| W   | 0.5     | 0.0     | 0.0           |
| D   | 0.0     | 0.5     | 0.0           |
| Q   | 0.0     | 0.0     | 0.25          |
| E   | 0.0     | 0.0     | -0.25         |

### Data Writer ###
This program records data coming from the simulation. To run it, use
```bash
./keyboard_controller
```
However, be advised that it writes data to whichever folder you are in when you call it. So it is recommended to
navigate to a dedicated folder before calling.

Each time an image is received, it writes the raw image to a PNG file with the name based on the current number of
images captures. (e.g. 000000.png, 000001.png, etc.). It also writes a similarly named file containing the pose of the
camera when the image is captured. This file is a CSV file named like 000000.txt, etc. The values are as follows.
```
x,y,z,roll,pitch,yaw
```
Lastly, the application writes the camera calibration information to file, with the name scheme 000000_calib.txt, etc.
While it is unlikely the calibration information will change during simulation, it is written at each instance just in
case. The output is more defined and describes each value before printing. An example is shown below.

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

Note that, because of the asynchronous nature of the data. The first pose or camera info files may be empty if they have
not been received prior to receiving an image.