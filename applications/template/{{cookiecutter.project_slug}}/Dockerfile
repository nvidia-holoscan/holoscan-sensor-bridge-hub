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

ARG BASE_IMAGE
ARG GPU_TYPE
FROM ${BASE_IMAGE} AS application-dev

ARG DEBIAN_FRONTEND=noninteractive
ARG PYTHON_VERSION=python3
ARG HOLOSCAN_CLI_INSTALL_SPEC=holoscan-cli==4.3.0a26390596878
ARG HOLOSCAN_CLI_INSTALL_EXTRA_FLAGS=--index-url https://test.pypi.org/simple/

RUN if ! command -v python3 >/dev/null 2>&1; then \
        apt-get update \
        && apt-get install --no-install-recommends -y \
            software-properties-common curl gpg-agent \
        && add-apt-repository ppa:deadsnakes/ppa \
        && apt-get update \
        && apt-get install --no-install-recommends -y \
            ${PYTHON_VERSION} \
        && apt-get purge -y python3-pip software-properties-common \
        && apt-get autoremove --purge -y \
        && rm -rf /var/lib/apt/lists/* \
        && update-alternatives --install /usr/bin/python python /usr/bin/${PYTHON_VERSION} 100 \
        && if [ "${PYTHON_VERSION}" != "python3" ]; then \
            update-alternatives --install /usr/bin/python3 python3 /usr/bin/${PYTHON_VERSION} 100; \
        fi; \
    fi

ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN if ! python3 -m pip --version >/dev/null 2>&1; then \
        apt-get update \
        && apt-get install --no-install-recommends -y curl ca-certificates \
        && curl -sS https://bootstrap.pypa.io/get-pip.py | ${PYTHON_VERSION} \
        && rm -rf /var/lib/apt/lists/*; \
    fi

RUN python3 -m pip install --no-cache-dir ${HOLOSCAN_CLI_INSTALL_EXTRA_FLAGS} "${HOLOSCAN_CLI_INSTALL_SPEC}"

RUN mkdir -p /tmp/scripts/utilities
COPY holohub /tmp/scripts/
COPY utilities/setup /tmp/scripts/utilities/setup/
COPY utilities/holohub_autocomplete /tmp/scripts/utilities/
RUN chmod +x /tmp/scripts/holohub
RUN /tmp/scripts/holohub setup && rm -rf /var/lib/apt/lists/*

RUN echo ". /etc/bash_completion.d/holohub_autocomplete" >> /etc/bash.bashrc

# This variable is consumed by dependencies as an environment variable at docker
# build time. It intentionally does not affect CMake builds performed at docker
# run time.
ARG CMAKE_BUILD_TYPE=Release

{% if cookiecutter.language == "python" %}
COPY applications/{{ cookiecutter.project_slug }}/requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt
{% endif %}

# TODO: Add any additional system dependencies required for {{ cookiecutter.project_name }}.

WORKDIR /workspace/holohub

ENV HOLOSCAN_INPUT_PATH=/workspace/holohub/data
# TODO: Add any application-specific environment variables here.
# ENV YOUR_APP_ENV_VAR=value

# TODO: Uncomment and modify the following if your application needs specific expose ports.
# EXPOSE 8080

# TODO: Uncomment and modify the following if your application needs a specific entrypoint.
# ENTRYPOINT ["./holohub", "run", "{{ cookiecutter.project_slug }}"]
