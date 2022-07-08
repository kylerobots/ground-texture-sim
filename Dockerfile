ARG UBUNTU_VERSION=focal
# Create a base image that is just the Ignition install.
FROM ubuntu:${UBUNTU_VERSION} AS base

LABEL author="Kyle M. Hart" \
	version="4.0.0" \
	license="SPDX-License-Identifier: GPL-3.0-or-later"

# Install Python and Blender
RUN apt update \
	&& DEBIAN_FRONTEND=noninteractive \
	apt install -y \
	blender \
	&& rm -rf /var/lib/apt/lists/*

# The development image will have development tools, like Git, installed.
FROM base AS dev

COPY requirements.dev.txt /tmp/

RUN apt update \
	&& DEBIAN_FRONTEND=noninteractive \
	apt install -y \
	doxygen \
	git \
	graphviz \
	python3-pip \
	&& rm -rf /var/lib/apt/lists/* \
	# Don't do a requirements file, since it is only needed for development.
	&& pip install --upgrade -r /tmp/requirements.dev.txt

CMD [ "blender" ]

FROM base AS run
# For some reason, the final run image needs Numpy installed explicitly, so do that here.
RUN apt update \
	&& DEBIAN_FRONTEND=noninteractive \
	apt install -y \
	python3-numpy \
	&& rm -rf /var/lib/apt/lists/*
# Make a local user
RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user/ground_texture_sim
COPY . /home/user/ground_texture_sim
ENV PYTHONPATH=/home/user/ground_texture_sim
CMD [ "blender", "example_setup/environment.blend", "-b", "--python", "generate_data.py", "--python-use-system-env", "--", "config.json" ]