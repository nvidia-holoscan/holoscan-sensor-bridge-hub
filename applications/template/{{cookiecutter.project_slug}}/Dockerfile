# syntax=docker/dockerfile:1

# SPDX-FileCopyrightText: Copyright (c) {{ cookiecutter.year }} {{ cookiecutter.full_name }}
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

############################################################
# Base image
############################################################

ARG BASE_IMAGE
ARG GPU_TYPE

FROM ${BASE_IMAGE} AS base

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        wget \
        xvfb \
        git \
        unzip \
        ffmpeg \
        ninja-build \
        libv4l-dev \
    && rm -rf /var/lib/apt/lists/*

# Use the same CLI pin as the host wrapper, including its shared build helpers.
COPY requirements-cli.txt /tmp/requirements-cli.txt
RUN python3 -m pip install --no-cache-dir --extra-index-url https://pypi.nvidia.com \
        --only-binary=:all: -r /tmp/requirements-cli.txt \
    && rm /tmp/requirements-cli.txt

# - This variable is consumed by all dependencies below as an environment variable (CMake 3.22+)
# - We use ARG to only set it at docker build time, so it does not affect cmake builds
#   performed at docker run time in case users want to use a different BUILD_TYPE
ARG CMAKE_BUILD_TYPE=Release

# --------------------------------------------------------------------------
#
# {{ cookiecutter.project_name }} specific dependencies
#
{% if cookiecutter.language == "python" %}
# Copy over app-specific requirements
COPY applications/{{ cookiecutter.project_slug }}/requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt
{% endif %}

# TODO: Add any additional system dependencies required for {{ cookiecutter.project_name }}
# Example:
# RUN apt update && apt install -y \
#     your-package-here \
#     another-package \
#     && rm -rf /var/lib/apt/lists/*

# TODO: Add any additional setup steps required for {{ cookiecutter.project_name }}
# Example:
# RUN your-setup-command-here

# --------------------------------------------------------------------------
#
# Application setup
#
WORKDIR /workspace/holoscan-sensor-bridge-hub

# Set default environment variables for the application
ENV HOLOSCAN_INPUT_PATH=/workspace/holoscan-sensor-bridge-hub/data
# TODO: Add any application-specific environment variables here
# ENV YOUR_APP_ENV_VAR=value

# TODO: Uncomment and modify the following if your application needs specific expose ports
# EXPOSE 8080

# TODO: Uncomment and modify the following if your application needs a specific entrypoint
# ENTRYPOINT ["./build/my_app/my_app"]
