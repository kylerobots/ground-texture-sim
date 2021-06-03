# Currently, Edifice targets Bionic (18.04) or Focal (20.04)
ARG UBUNTU_VERSION=focal
FROM ubuntu:${UBUNTU_VERSION} as dev

# Install Ignition Edifice and its dependencies. Because of the install via new key, 2 installs are required. One for
# the dependecies and one for the package after the dependencies are used to add the key.
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && \
	apt install -y \
	gnupg \
	lsb-release \
	wget && \
	echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list && \
	wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - && \
	apt update && \
	apt install -y ignition-edifice && \
	rm -rf /var/lib/apt/lists/*

# Start up a simple test environment for now.
CMD [ "ign", "gazebo", "shapes.sdf" ]