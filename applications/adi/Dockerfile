# syntax=docker/dockerfile:1
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

#ARG BASE_IMAGE=nvcr.io/nvidia/clara-holoscan/holoscan:v4.4.0-cuda13@sha256:7af522a5ab43f5be6503520dc2afda1f4690b55079ebaca125910a1ec0d3df19
#ARG BASE_IMAGE=nvcr.io/nvidia/clara-holoscan/holoscan:v4.6.0-cuda13
#FROM ${BASE_IMAGE}
ARG GPU_TYPE
ARG BASE_SDK_VERSION
ARG BASE_IMAGE=nvcr.io/nvidia/clara-holoscan/holoscan:v${BASE_SDK_VERSION}-${GPU_TYPE}
FROM ${BASE_IMAGE} AS base

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
      git ninja-build libyaml-cpp-dev libcurl4-openssl-dev libssl-dev \
      libfmt-dev libnuma-dev libelf-dev libvulkan-dev \
    && rm -rf /var/lib/apt/lists/*

# Install basic dependencies
RUN apt update && apt install -y \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Add ROS2 Jazzy repository
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS2 Jazzy and Vulkan support (required for HolovizOp in subscriber)
# Also install libcurl and libssl required by programmer.cpp (firmware update)
RUN apt update && apt install -y \
    ros-jazzy-desktop \
    ros-jazzy-ros-base \
    ros-jazzy-ros-core \
    ros-jazzy-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

COPY applications/adi/prepare_hsb.py /opt/adi/prepare_hsb.py
COPY applications/adi/patches /opt/adi/patches
RUN python3 /opt/adi/prepare_hsb.py /opt/hsb

COPY applications/adi /opt/adi
ARG CUDA_ARCHITECTURES=89
ARG BUILD_JOBS=4
RUN cmake -S /opt/adi -B /opt/adi/build -G Ninja \
      -DHSB_SOURCE_DIR=/opt/hsb \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_CUDA_ARCHITECTURES=${CUDA_ARCHITECTURES} \
      -DCMAKE_INSTALL_PREFIX=/opt/adi/install \
    && cmake --build /opt/adi/build --parallel ${BUILD_JOBS} \
    && cmake --install /opt/adi/build

# The apt-installed scipy is compiled against NumPy 1.x but the base image ships
# NumPy 2.x.  CuPy imports cupyx.scipy → scipy.sparse which triggers a
# "numpy.dtype size changed" binary incompatibility at import time.
# --ignore-installed installs a NumPy 2.x-compatible wheel into
# /usr/local/lib/python3.12/dist-packages/ without trying to remove the
# apt-managed package (which has no RECORD file and cannot be uninstalled by pip).
# Python resolves /usr/local/lib before /usr/lib so the new wheel takes precedence.
RUN pip3 install --ignore-installed scipy
# Required by Python publisher firmware update (manifest download + YAML parse)
RUN pip3 install requests pyyaml

# Reuse the repository's CLI pin when entering this image through ./hsb.
COPY requirements-cli.txt /tmp/requirements-cli.txt
COPY applications/adi/requirements.txt /tmp/requirements-adi.txt
RUN python3 -m pip install --no-cache-dir --break-system-packages \
      --extra-index-url https://pypi.nvidia.com \
      --only-binary=:all: -r /tmp/requirements-cli.txt -r /tmp/requirements-adi.txt \
    && rm /tmp/requirements-cli.txt /tmp/requirements-adi.txt

ENV PATH=/opt/adi/install/bin:${PATH}
ENV PYTHONPATH=/opt/adi/install/python:${PYTHONPATH}

# Set ROS2 environment variables
ENV ROS_DISTRO=jazzy
ENV ROS_VERSION=2
ENV ROS_PYTHON_VERSION=3
ENV ROS_DOMAIN_ID=5
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ENV CYCLONEDDS_URI=file:///opt/adi/adi_imu/app/config.xml
ENV CMAKE_PREFIX_PATH=/opt/ros/jazzy:/opt/nvidia/holoscan
ENV AMENT_PREFIX_PATH=/opt/ros/jazzy
ENV LD_LIBRARY_PATH=/opt/ros/jazzy/lib:$LD_LIBRARY_PATH
ENV PATH=/opt/ros/jazzy/bin:$PATH
ENV PKG_CONFIG_PATH=/opt/ros/jazzy/lib/pkgconfig
RUN echo -e '#!/bin/bash \n \
set -e \n \
source /opt/ros/jazzy/setup.bash \n \
exec "$@"' > /usr/bin/entrypoint.sh && chmod +x /usr/bin/entrypoint.sh

ENTRYPOINT ["/usr/bin/entrypoint.sh"]

WORKDIR /opt/adi
CMD ["bash"]
