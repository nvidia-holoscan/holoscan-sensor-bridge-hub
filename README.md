# Holoscan Sensor Bridge Hub

A focused collection of reference applications, operators, and tutorials for [Holoscan Sensor Bridge](https://docs.nvidia.com/holoscan/sensor-bridge/latest/index.html) and related sensor I/O on the Holoscan platform.

![Lint](https://img.shields.io/github/actions/workflow/status/nvidia-holoscan/holoscan-sensor-bridge-hub/check_lint.yml?branch=main&label=Lint)
![Metadata](https://img.shields.io/github/actions/workflow/status/nvidia-holoscan/holoscan-sensor-bridge-hub/check_metadata.yml?branch=main&label=Metadata)

*note*: For other components in the NVIDIA Holoscan ecosystem, see [Holohub](https://github.com/nvidia-holoscan/holohub) and [nvidia-holoscan.github.io/holohub](https://nvidia-holoscan.github.io/holohub).

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Building](#container-build-recommended)
- [Running](#running-applications)
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
- Python 3.10+ on the host for the `holohub` wrapper
- NVIDIA NGC credentials at [ngc.nvidia.com](https://catalog.ngc.nvidia.com/)

The `./holohub` wrapper delegates to the standalone `holoscan-cli` package. If
`holoscan-cli` is not importable, the wrapper installs it with `pip` on first
use. The wrapper pins the current prerelease wheel from TestPyPI:

```sh
HOLOSCAN_CLI_VERSION=holoscan-cli==4.3.0a26390596878 \
HOLOSCAN_CLI_INSTALL_EXTRA_FLAGS="--index-url https://test.pypi.org/simple/" \
./holohub --help
```

#### Fetch

```sh
git clone https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub.git
cd holoscan-sensor-bridge-hub
```

#### HoloHub run command (recommended)

```sh
./holohub run <application_name>
```

See each project's `README.md` and `metadata.json` for dependencies and hardware requirements.

#### Build

```sh
./holohub build-container [project_name]
```

See [`doc/developer.md`](./doc/developer.md) for native build and development details.

## Running

```sh
./holohub run <application_name>
```

## Contributing

Please review [CONTRIBUTING.md](./CONTRIBUTING.md). New projects should use `./holohub create` and the `template/` folders under each component directory.

## More Information

- [Holohub](https://github.com/nvidia-holoscan/holohub) — main reference catalog (part of which this repo is)
- [Holoscan Sensor Bridge](https://github.com/nvidia-holoscan/holoscan-sensor-bridge)
- [Holoscan SDK User Guide](https://docs.nvidia.com/holoscan/sdk-user-guide/overview.html)
