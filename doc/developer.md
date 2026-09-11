# Holoscan Sensor Bridge Hub Developer Reference

In this guide we aim to document advanced workflows to aid developers working in Holoscan Sensor Bridge Hub,
and to support advanced project use cases.

## Table of Contents

- [CLI Setup](#cli-setup)
- [Native Build](#native-build)
- [Container Build](#container-build)
- [Running Applications](#running-applications)

## CLI Setup

`./hsb` delegates to [Holoscan CLI](https://github.com/nvidia-holoscan/holoscan-cli),
pinned in `requirements-cli.txt` to `5.0.0a1` from `https://pypi.nvidia.com`.
The `create` extra installs Cookiecutter and metadata validation dependencies from
PyPI so `./hsb create` works on first use. Python 3.11–3.13 with `venv` and `pip`
is required.

The wrapper configures the repository, selects Python, activates that interpreter
for child commands, and verifies or installs the pinned CLI. An explicit
`HOLOSCAN_CLI_PYTHON_BIN=/path/to/python` takes priority over an active virtual
environment. Missing packages are installed into the selected environment.

Otherwise, hosts automatically use a managed virtual environment at
`$XDG_CACHE_HOME/holoscan-cli/5.0.0a1/py3.12/venv` (with the selected Python minor
version in place of `py3.12`); the cache defaults to `~/.cache`. Set
`HOLOSCAN_CLI_VENV` to choose a different location. No manual activation or `sudo`
is needed.

The development and application-template Dockerfiles install the same CLI pin
and creation dependencies while building the image. Inside the container, `./hsb` reuses that installation
and applies the hub's paths. The CLI sets `HOLOSCAN_CLI_BUILD_LOCAL=1` when launching
the container, so inner build and run commands execute locally.
An outdated image missing the pinned CLI or creation dependencies reports that
it needs rebuilding. It does not install into the mounted checkout by default.

```sh
./hsb --help
./hsb version
./hsb list
```

Use `--dryrun --verbose` to preview build and run commands. The initial CLI
installation still takes place when previewing a command; subsequent invocations
reuse the installed package.

The SDK container defaults to version `4.6.0`, separately from the CLI version.
Set `HOLOSCAN_CLI_BASE_SDK_VERSION` to choose another SDK release, or pass
`--base-img <sdk-image>` for an exact image. Check each project's hardware and SDK
requirements before building.

Shared CMake macros, metadata schemas and helpers, setup scripts, and the CTest
driver come from this package. CMake invokes `./hsb version --json` to locate the
pinned package, including when configuring directly with `cmake`. The local
`cmake/` directory contains only helpers not supplied by the CLI.

Metadata utilities keep the hub's directory checks and README summaries. In a
Python virtual environment or development container, install their dependencies
and run the same checks used by CI:

```sh
python3 -m pip install -r utilities/requirements.txt
python3 -m utilities.metadata.metadata_validator
python3 -m utilities.metadata.gather_metadata
```

## Native Build

### Software Prerequisites (Native)

Refer to the [Holoscan SDK README](https://github.com/nvidia-holoscan/holoscan-sdk/blob/main/README.md) for ways to install Holoscan SDK in local environment: Debian package, Python wheels or from source.

Install the package dependencies on your host system. Typical requirements include:

- [CMake](https://www.cmake.org): 3.24.0+
- Python interpreter and development headers matching your SDK; the CLI requires Python 3.11–3.13
- ffmpeg runtime
- [ngc-cli](https://ngc.nvidia.com/setup/installers/cli)
- wget
- CUDA Toolkit: 12.6
- libcudnn9-cuda-12
- libcudnn9-dev-cuda-12
- libnvinfer-dev
- libnvinfer-plugin-dev
- libnvonnxparsers-dev

Visit the [Holoscan SDK User Guide](https://docs.nvidia.com/holoscan/sdk-user-guide/sdk_installation.html) for the latest
details on dependency versions and custom installation.

*Note: Other applications might require more dependencies. Please refer to the README of each application for more information.*

### Building with CMake

Configure and build a specific application from the repository root:

```bash
./hsb build <application_name> --local --dryrun --verbose
./hsb build <application_name> --local
```

Or use CMake directly:

```bash
cmake -B build -S . -DAPP_<application_name>=ON
cmake --build build
```

Replace `<application_name>` with the project name (for example, `APP_my_app=ON`).

## Container Build

Build the default development container from the repository root:

```sh
./hsb build-container --dryrun --verbose
./hsb build-container
```

Build a specific Dockerfile stage (for example, AJA development):

```sh
./hsb build-container --build-args="--target holohub-aja" --img holoscan-sensor-bridge-hub:aja --dryrun --verbose
./hsb build-container --build-args="--target holohub-aja" --img holoscan-sensor-bridge-hub:aja
```

Launch an interactive development container with the repository mounted:

```sh
./hsb run-container --dryrun --verbose
./hsb run-container
```

Projects may provide their own `Dockerfile`; check each project's `metadata.json` and README for details.

## Running Applications

Each application defines run instructions in its `README.md` and `metadata.json`:

```sh
./hsb run <application_name> --dryrun --verbose
./hsb run <application_name>
```

Inside the development container, the CLI uses the mounted `./hsb` wrapper and
builds and runs locally. Use `--local` for a native host environment.

The repository creates a `data` subdirectory under the build directory to store downloaded datasets.
This directory is noted as `HOLOHUB_DATA_DIR` / `<holohub_data_dir>` in documentation, READMEs, and metadata files.

For profiling with Nsight Systems, run applications with `nsys profile` inside the development container and inspect the generated report with `nsys-ui`.
