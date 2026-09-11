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
| --- | --- |
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
- Python 3.11–3.13 with `venv` and `pip` for the `./hsb` CLI
- NVIDIA NGC credentials at [ngc.nvidia.com](https://catalog.ngc.nvidia.com/)

#### Fetch

```sh
git clone https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub.git
cd holoscan-sensor-bridge-hub
```

See each project's `README.md` and `metadata.json` for dependencies and hardware requirements.

## Building

Use `./hsb` to discover, build, and run projects. On first use it installs
`holoscan-cli[create]==5.0.0a1`, including template dependencies, into a managed
virtual environment under `$XDG_CACHE_HOME/holoscan-cli/` or `~/.cache/holoscan-cli/`.
An active virtual environment or `HOLOSCAN_CLI_PYTHON_BIN` selects an existing
Python environment instead. Containers reuse the image's installed CLI.
No virtual environment activation is needed.

```sh
./hsb --help
./hsb list
```

The repository currently contains scaffolding templates; `list` will be empty
until projects with `metadata.json` are added. Templates are excluded from discovery.
See [Starting a New Project](./applications/README.md#starting-a-new-project) to
generate a C++ or Python application with `./hsb create`.

Build the default development container:

```sh
./hsb build-container --dryrun --verbose
./hsb build-container
```

The wrapper defaults to Holoscan SDK 4.6.0 and lets the CLI select the CUDA tag.
Use `--base-img <sdk-image>` to select the image required by your hardware or project.
CLI and SDK image versions are configured independently.

For a contributed project, use `./hsb build <project>`; the CLI reads the Dockerfile
and dependencies from that project's `metadata.json`.

See [`doc/developer.md`](./doc/developer.md) for native build and development details.

## Running

Open the development container with the repository mounted:

```sh
./hsb run-container --dryrun --verbose
./hsb run-container
```

Run a contributed application with `./hsb run <project>`. Follow its `README.md`
for sensor setup, data downloads, and hardware requirements.

## Contributing

Please review [CONTRIBUTING.md](./CONTRIBUTING.md). New projects should use the `template/` folders under each component directory.

## More Information

- [Holohub](https://github.com/nvidia-holoscan/holohub) — main reference catalog (part of which this repo is)
- [Holoscan Sensor Bridge](https://github.com/nvidia-holoscan/holoscan-sensor-bridge)
- [Holoscan SDK User Guide](https://docs.nvidia.com/holoscan/sdk-user-guide/overview.html)
