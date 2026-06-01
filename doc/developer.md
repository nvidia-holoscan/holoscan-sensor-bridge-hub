# HoloHub Developer Reference

In this guide we aim to document advanced workflows to aid developers working in Holoscan Sensor Bridge Hub,
and to support advanced project use cases.

## Table of Contents

- [Native Build](#native-build)
- [Container Build](#container-build)
- [Running Applications](#running-applications)

## Native Build

### Software Prerequisites (Native)

Refer to the [Holoscan SDK README](https://github.com/nvidia-holoscan/holoscan-sdk/blob/main/README.md) for ways to install Holoscan SDK in local environment: Debian package, Python wheels or from source.

Install the package dependencies on your host system. Typical requirements include:

- [CMake](https://www.cmake.org): 3.24.0+
- Python interpreter: 3.9 to 3.12
- Python dev: 3.9 to 3.12 (matching version of the interpreter)
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
cmake -B build -S . -DAPP_<application_name>=ON
cmake --build build
```

Replace `<application_name>` with the project name (for example, `APP_my_app=ON`).

## Container Build

Build the default development container from the repository root:

```sh
docker build -t holoscan-sensor-bridge-hub:dev .
```

Build a specific Dockerfile stage (for example, AJA development):

```sh
docker build --target holohub-aja -t holoscan-sensor-bridge-hub:aja .
```

Launch an interactive development container with the repository mounted:

```sh
docker run --gpus all -it --rm \
  -v "$(pwd)":/workspace/holoscan-sensor-bridge-hub \
  -w /workspace/holoscan-sensor-bridge-hub \
  holoscan-sensor-bridge-hub:dev
```

Projects may provide their own `Dockerfile`; check each project's `metadata.json` and README for details.

## Running Applications

Each application defines run instructions in its `README.md` and `metadata.json`. After building inside a container or native environment, run the application binary or script as documented for that project.

The repository creates a `data` subdirectory under the build directory to store downloaded datasets.
This directory is noted as `HOLOHUB_DATA_DIR` / `<holohub_data_dir>` in documentation, READMEs, and metadata files.

For profiling with Nsight Systems, run applications with `nsys profile` inside the development container and inspect the generated report with `nsys-ui`.
