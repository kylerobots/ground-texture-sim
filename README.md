# Ground Texture Simulation
This package provides an Ignition simulation of realistic ground texture for use by monocular SLAM applications. To
promote fidelity, it uses physics based rendering (PBR) to accurately simulate the appearance of the ground texture.
Additionally, it avoids the repetition of tiles common in most simulated floors.

[Source Code](https://github.com/kylerobots/ground-texture-sim)

[Documentation](https://kylerobots.github.io/ground-texture-sim/)

## License ##
This project is licensed, under the BSD 3-Clause "New" or "Revised" License. See [LICENSE](LICENSE.md) for more info.

## Installing and Running with Docker ##
Using the Docker images defined with the project is by far the easiest route, as it avoids all the installation. The
already built image is available at https://hub.docker.com/repository/docker/kylerobots/ground-texture-sim. The version
tags match the release versions. The *latest* tag matches the current tip of the *main* branch, which is not
necessarily a tagged version. You can also build the image from the source code. The *run* stage has a minimal image
that provides all needed code and simulation files. If you are building locally, use something like the following to
build. The *BUILD_TEST* argument controls if unit tests are compiled (ON) or not (OFF).
```powershell
docker build --build-arg BUILD_TEST=OFF --target run -t ground-texture-sim:run .
```
The online repository image and the one built in the previous command both have a default command that starts the
correct launch file. This launch file starts the simulation and trajectory control. It can be started by running the
following, which uses the same image tag as the online repository. This assumes a Windows host, so defines the needed
DISPLAY variable to show the GUI correctly.
```powershell
docker run -e DISPLAY=host.docker.internal:0.0 kylerobots/ground-texture-sim:1.1.0
```

When working from source, there is also a *test* stage if you wish to run the unit tests. Commands are similar to above.
```powershell
docker build --build-arg BUILD_TEST=ON --target test -t ground-texture-sim:test .
docker run ground-texture-sim:test
```

## Installing and Running Locally ##
If you wish to install on your computer, you will need a system running Ubuntu 20.04 or 16.04. This is because the
simulation uses Ignition Gazebo, which only works on those OS versions at the moment. Specifically, this has been tested
with Ignition Edifice. You will need the below dependencies. Most are just to support compilation.

* cmake *(installed via apt)*
* build-essential *(installed via apt)*
* git *(installed via apt)*
* wget *(installed via apt)*
* ignition edifice *(see [their documentation](https://www.ignitionrobotics.org/docs/edifice/install_ubuntu) for install
instructions)*

After installing the dependencies, run the following commands from wherever you want to put the source code. You can
turn unit tests back on by changing DBUILD_TESTING to *on*.
```bash
git clone https://github.com/kylerobots/ground-texture-sim.git
mkdir ground-texture-sim/build
cd ground-texture-sim/build
cmake -DBUILD_TESTING=off -DCMAKE_BUILD_TYPE=Release ..
make -j
make install
```

There is a launch file that starts everything automatically, so you only need to run the following.
```bash
ign launch launch/trajectory.ign
```
You can also start each node individually if you prefer. See below for details on each.

## Node Descriptions ##

### Simulation ###
To start the Gazebo simulation, run this from the root level of the code:
```bash
ign gazebo world/world.sdf
```
You should see the GUI appear with a camera feed, like so.

![Example GUI](./GUI.png "The Simulation GUI")

### Trajectory Follower ###
This is the preferred node for capturing data. It walks the camera through a series of predefined poses and captures
data at each pose. To start, run this command:
```bash
follow_trajectory
```
The trajectory is read from a CSV file called *data/trajectory.txt* located relative to where the code runs. The built
Docker image has an example file that it copies in. Poses should be specified one per line in the following format.
```
x1, y1, yaw1
x2, y2, yaw2
```
Extra values per line will be ignored. If an error occurs on read, the system halts.

### Data Writing ###
While not a unique node, it is important to cover how the data is written to file. Be advised that the program
writes data to whichever folder you are in when you call it. So it is recommended to navigate to a dedicated folder
before calling.

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
