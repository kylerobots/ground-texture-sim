# Currently, Ignition targets Bionic (18.04) or Focal (20.04) so valid values are: bionic, 18.04, focal, 20.04
ARG UBUNTU_VERSION=focal
# Create a base image that is just the Ignition install.
FROM ubuntu:${UBUNTU_VERSION} AS base

LABEL author="Kyle M. Hart" \
	version="2.1.0" \
	license="BSD-3-Clause License"

# Install Ignition and its dependencies. Because of the install via new key, 2 installs are required. One for the
# dependecies and one for the package after the dependencies are used to add the key. Valid Ignition versions are the
# ones that have PBR rendering: citadel, dome, edifice
ARG IGNITION_VERSION=edifice
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
	apt install -y \
	build-essential \
	cmake \
	# Git is needed for development, but also to clone GTest for testing while building. It isn't needed during
	# deployment though, so maybe it should be installed then uninstalled during building.
	git \
	lsb-release \
	wget && \
	echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list && \
	wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - && \
	apt update && \
	apt install -y ignition-${IGNITION_VERSION} && \
	rm -rf /var/lib/apt/lists/*

# Start up a simple test environment for now.
CMD [ "ign", "gazebo", "shapes.sdf" ]

# The development image will have development tools, like Git, installed.
FROM base AS dev

RUN apt update && \
	DEBIAN_FRONTEND=noninteractive \
	apt install -y \
	doxygen \
	gdb \
	graphviz && \
	rm -rf /var/lib/apt/lists/*

# Use an image to compile and install the package.
FROM base AS build
COPY . /opt/ground-texture-sim
WORKDIR /opt/ground-texture-sim/build
ARG BUILD_TEST=OFF
RUN cmake -DBUILD_TESTING=${BUILD_TEST} -DCMAKE_BUILD_TYPE=Release -S /opt/ground-texture-sim -B /opt/ground-texture-sim/build && \
	make -j && \
	make install
CMD [ "ctest", "-VV" ]

# From the compiled version, copy over the applications needed to run.
FROM base AS run
COPY --from=build /usr/local/ /usr/local/
# Make a local user.
RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user
# Copy in the sdf file.
COPY config/ /home/user/config/
COPY launch/ /home/user/launch/
COPY world/ /home/user/world/
CMD [ "ign", "launch", "launch/generate_data.ign", "trajectory:=config/trajectory.txt" ]