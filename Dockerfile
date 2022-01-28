ARG UBUNTU_VERSION=focal
# Create a base image that is just the Ignition install.
FROM ubuntu:${UBUNTU_VERSION} AS base

LABEL author="Kyle M. Hart" \
	version="3.0.0" \
	license="SPDX-License-Identifier: GPL-3.0-or-later"

# Install Python and Blender
RUN apt update \
	&& DEBIAN_FRONTEND=noninteractive \
	apt install -y \
	blender \
	&& rm -rf /var/lib/apt/lists/*

# The development image will have development tools, like Git, installed.
FROM base AS dev

RUN apt update \
	&& DEBIAN_FRONTEND=noninteractive \
	apt install -y \
	doxygen \
	git \
	graphviz \
	python3-pip \
	&& rm -rf /var/lib/apt/lists/* \
	# Don't do a requirements file, since it is only needed for development.
	&& pip install --upgrade \
	autopep8 \
	pylint

CMD [ "blender" ]