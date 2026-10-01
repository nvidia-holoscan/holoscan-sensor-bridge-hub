# Holoscan Sensor Bridge Hub

A curated collection of sensor integrations, demos, and related projects for [Holoscan Sensor Bridge](https://github.com/nvidia-holoscan/holoscan-sensor-bridge) (HSB), from NVIDIA and ecosystem partners.

[![Check linting](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/actions/workflows/check_lint.yml/badge.svg?branch=main)](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/actions/workflows/check_lint.yml)
[![Check metadata validity](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/actions/workflows/check_metadata.yml/badge.svg?branch=main)](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/actions/workflows/check_metadata.yml)
[![Check Compliance](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/actions/workflows/check_compliance.yml/badge.svg?branch=main)](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/actions/workflows/check_compliance.yml)
[![Check URLs](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/actions/workflows/check_urls.yml/badge.svg?branch=main)](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/actions/workflows/check_urls.yml)

*note*: For other components in the NVIDIA Holoscan ecosystem, see [Holohub](https://github.com/nvidia-holoscan/holohub) and [nvidia-holoscan.github.io/holohub](https://nvidia-holoscan.github.io/holohub).

## Table of Contents

- [Repository Organization](#repository-organization)
- [Getting Started](#getting-started)
- [Linting](#linting)
- [Contributing](#contributing)
- [More Information](#more-information)

## Repository Organization

Projects are grouped by the organization that maintains them, under `<org>/<category>/<project>/`:

```text
holoscan-sensor-bridge-hub/
├── nvidia/
│   ├── examples/template_app/   # application template
│   └── operators/template_op/   # operator template
├── <org>/                       # for example adi/ or altera/
│   └── <category>/<project>/
└── tools/                       # opt-in shared helpers and CI checks
```

Categories are `operators`, `examples`, `demos`, `fpga`, `ai/skills`, `benchmarks`, `tutorials`, and `utilities`. Organization and category folders are created with their first project.

Each project is self-contained: it builds on its own, and its `README.md` lists the hardware, the tested Holoscan Sensor Bridge and Holoscan SDK versions, and the build, run, and test commands. Each project is maintained by its contributor; hosting a project here does not imply NVIDIA certification or maintenance.

## Getting Started

Most projects run on an HSB setup. Before building one, follow the HSB user guide to set up the [hardware](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/hardware-setup) and the [host](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/host-setup), and to [build the HSB container](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/build) from the [HSB release](https://github.com/nvidia-holoscan/holoscan-sensor-bridge/releases) listed in the project's `README.md`. Then follow the project's `README.md`.

To start a new project, copy the [application template](./nvidia/examples/template_app/) or the [operator template](./nvidia/operators/template_op/). Shared, opt-in helpers such as CMake modules and a development container are described in [`tools/`](./tools/README.md).

## Linting

Install the lint tools in a virtual environment and run all checks from the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r tools/lint/requirements.txt
.venv/bin/pre-commit run --all-files
```

The virtual environment avoids the `externally-managed-environment` error that `pip install` raises on systems with an externally managed Python. Many hooks fix issues in place; rerun the last command until it passes. CI runs the same checks, plus copyright, link, and `metadata.json` checks. See [CONTRIBUTING.md](./CONTRIBUTING.md#linting) for more on the setup.

## Contributing

Please review [CONTRIBUTING.md](./CONTRIBUTING.md) for project requirements, ownership, and the review process.

## More Information

- [Holoscan Sensor Bridge](https://github.com/nvidia-holoscan/holoscan-sensor-bridge) and its [releases](https://github.com/nvidia-holoscan/holoscan-sensor-bridge/releases)
- [Holoscan Sensor Bridge user guide](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/introduction)
- [Holoscan SDK User Guide](https://docs.nvidia.com/holoscan/sdk-user-guide/overview.html)
- [Holohub](https://github.com/nvidia-holoscan/holohub)
