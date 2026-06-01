# Holoscan Sensor Bridge Hub

A focused collection of reference applications, operators, and tutorials for [Holoscan Sensor Bridge](https://docs.nvidia.com/holoscan/sensor-bridge/latest/index.html) and related sensor I/O on the Holoscan platform.

![Lint](https://img.shields.io/github/actions/workflow/status/nvidia-holoscan/holoscan-sensor-bridge-hub/check_lint.yml?branch=main&label=Lint)
![Metadata](https://img.shields.io/github/actions/workflow/status/nvidia-holoscan/holoscan-sensor-bridge-hub/check_metadata.yml?branch=main&label=Metadata)

*note*: For other components in the NVIDIA Holoscan ecosystem, see [Holohub](https://github.com/nvidia-holoscan/holohub) and [nvidia-holoscan.github.io/holohub](https://nvidia-holoscan.github.io/holohub).

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Building](#building)
- [Running](#running)
- [Contributing](#contributing)
- [More Information](#more-information)

## Overview

| Directory | Purpose |
|-----------|---------|
| [`applications/`](./applications/) | Example Holoscan applications for Sensor Bridge use cases |
| [`operators/`](./operators/) | Reusable Holoscan operators |
| [`tutorials/`](./tutorials/) | Walkthroughs and how-tos |

Each project includes a `metadata.json` and `README.md`. Use the `template/` folder in each directory to start a new project.

## Prerequisites

Refer to the [Holoscan SDK User Guide](https://docs.nvidia.com/holoscan/sdk-user-guide/sdk_installation.html#prerequisites) and the [Holoscan Sensor Bridge documentation](https://docs.nvidia.com/holoscan/sensor-bridge/latest/index.html) for platform and hardware requirements.

### Container Build (Recommended)

- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- [Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) with buildx
- `git`
- NVIDIA NGC credentials at [ngc.nvidia.com](https://catalog.ngc.nvidia.com/)

#### Fetch

```sh
git clone https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub.git
cd holoscan-sensor-bridge-hub
```

See each project's `README.md` and `metadata.json` for dependencies and hardware requirements.

#### Build

Build the default development container:

```sh
docker build -t holoscan-sensor-bridge-hub:dev .
```

Or build a project-specific container using the Dockerfile path in that project's `metadata.json`.

See [`doc/developer.md`](./doc/developer.md) for native build and development details.

## Running

Follow the instructions in each application's `README.md`. Applications typically define a run command in `metadata.json` that can be executed inside the development container.

## Contributing

Please review [CONTRIBUTING.md](./CONTRIBUTING.md). New projects should use the `template/` folders under each component directory.

## More Information

- [Holohub](https://github.com/nvidia-holoscan/holohub) — main reference catalog (part of which this repo is)
- [Holoscan Sensor Bridge](https://github.com/nvidia-holoscan/holoscan-sensor-bridge)
- [Holoscan SDK User Guide](https://docs.nvidia.com/holoscan/sdk-user-guide/overview.html)
