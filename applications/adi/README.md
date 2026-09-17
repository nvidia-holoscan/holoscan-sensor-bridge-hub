# ADI Sensors

ADI time-of-flight (ToF), industrial IMU, and A2B audio examples built with
Holoscan Sensor Bridge (HSB). This directory provides a standalone CMake build
and a Docker workflow. No Hub CLI is required.

The existing `./hsb` wrapper can also build the image and open a development
container; both entry points use the same Dockerfile.

## Source versions

- HSB release **2.7.0**, commit `1df133d4c78a6921249be4b147d65554aa8efa68`.
- ADI examples imported from
  [sibsankardey/holoscan-sensor-bridge](https://github.com/sibsankardey/holoscan-sensor-bridge/tree/9c8221090c1e6174ddce79c05666d94a3c16c869/examples/adi),
  commit `9c8221090c1e6174ddce79c05666d94a3c16c869`.
- Container: Holoscan SDK **4.4.0**, CUDA **13**.

The examples retain their original NVIDIA and Analog Devices license notices.
Build integration changes are maintained in this directory.

## Build on x86_64

Install Docker and the NVIDIA Container Toolkit. Run from the Hub repository root:

```sh
docker build --progress=plain \
  -f applications/adi/Dockerfile \
  --build-arg CUDA_ARCHITECTURES=89 \
  --build-arg BUILD_JOBS=4 \
  -t hsb-adi:2.7.0 .
```

Architecture `89` targets Ada GPUs. Set `CUDA_ARCHITECTURES` to the compute
capability of your deployment GPU; building does not require GPU access.
This Dockerfile targets x86_64 with CUDA 13. Jetson/IGX/ARM builds need a matching
platform environment and are not covered by this container recipe.

The build prepares an HSB checkout in `/opt/hsb`, applies the two ADI patches,
and compiles HSB and the ADI examples together. It installs the results under
`/opt/adi/install`. Linux socket receivers are used; RoCE and DOCA are disabled
by default so a ConnectX adapter is not needed to build or run the smoke checks.

## Verify the installation

```sh
docker run --rm --gpus all --ulimit stack=67108864 hsb-adi:2.7.0 \
  ctest --test-dir /opt/adi/build --output-on-failure
docker run --rm --gpus all --ulimit stack=67108864 hsb-adi:2.7.0 \
  python3 /opt/adi/smoke_test.py
```

These checks run the C++ and Python player help and import the installed
Hololink and IMU bindings. They do not acquire sensor data. ROS2 is not installed in this image.

## Optional HSB CLI

From the Hub repository root:

```sh
adi_sdk_image=nvcr.io/nvidia/clara-holoscan/holoscan:v4.4.0-cuda13@sha256:7af522a5ab43f5be6503520dc2afda1f4690b55079ebaca125910a1ec0d3df19
./hsb build-container adi --base-img "$adi_sdk_image" --img hsb-adi:2.7.0 --dryrun --verbose
./hsb build-container adi --base-img "$adi_sdk_image" --img hsb-adi:2.7.0
./hsb run-container adi --img hsb-adi:2.7.0 --no-docker-build --dryrun --verbose \
  -- python3 /opt/adi/smoke_test.py
./hsb run-container adi --img hsb-adi:2.7.0 --no-docker-build \
  -- python3 /opt/adi/smoke_test.py
```

The container already contains the built examples. To rebuild edited Hub
sources in the mounted workspace:

```sh
./hsb build adi --img hsb-adi:2.7.0 --no-docker-build --parallel 4 \
  --configure-args=-DCMAKE_CUDA_ARCHITECTURES=89 --dryrun --verbose
./hsb build adi --img hsb-adi:2.7.0 --no-docker-build --parallel 4 \
  --configure-args=-DCMAKE_CUDA_ARCHITECTURES=89
```

This uses the patched `/opt/hsb` dependency from the image. The standalone
CMake workflow below can use a separately prepared checkout.
The explicit base image keeps the CLI's repository-wide SDK default from
overriding the version validated for these examples.

## Run with hardware

Configure the host sensor network and firmware using the sensor-specific guide.
Inspect the available options with:

```sh
docker run --rm -it --gpus all --network host hsb-adi:2.7.0 \
  adcam_player --help
docker run --rm -it --gpus all --network host hsb-adi:2.7.0 \
  audio_viz_disp --help
```

Use the options shown by each executable to select the sensor IP, operating
mode, and headless/display behavior. Display output additionally needs the host
display connection configured for Docker.

- [ToF camera and firmware guide](aditof/README.md)
- [IMU and ROS2 guide](adi_imu/README.adi_imu_ros.md)
- [A2B audio guide](a2baudio/README.audio_viz_dsp.md)

The imported guides describe the original in-tree HSB layout. Use the build
commands above for this Hub integration. In this image, their `examples/adi/`
source paths correspond to `/opt/adi/`; C++ executables are already on `PATH`.

## Build with a local HSB checkout

Inside a compatible development environment containing the Dockerfile's dependencies:

```sh
python3 applications/adi/prepare_hsb.py build/adi-hsb-source
cmake -S applications/adi -B build/adi-standalone -G Ninja \
  -DHSB_SOURCE_DIR="$PWD/build/adi-hsb-source" \
  -DCMAKE_CUDA_ARCHITECTURES=89 \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="$PWD/install/adi-standalone"
cmake --build build/adi-standalone --parallel 4
cmake --install build/adi-standalone
ctest --test-dir build/adi-standalone --output-on-failure
PATH="$PWD/install/adi-standalone/bin:$PATH" \
PYTHONPATH="$PWD/install/adi-standalone/python${PYTHONPATH:+:$PYTHONPATH}" \
  python3 applications/adi/smoke_test.py
```

`prepare_hsb.py` clones the release into a new directory, verifies its commit,
and applies the patch after `git apply --check`. Repeating it is supported.
An existing checkout at a different revision is rejected without being reset.
For development, `HSB_SOURCE_DIR` can point directly to your own patched HSB
checkout; compatibility with other revisions must be checked by the developer.

## Hardware patches

[`patches/0001-adi-spi-gpio.patch`](patches/0001-adi-spi-gpio.patch) carries the
changes from ADI's fork:

- Advertise 32 GPIOs for the hololink-lite enumeration strategy, including the
  GPIO used for the Lattice camera reset.
- Allow SPI command lengths below 64 bytes instead of below 16 bytes.

These are partner-specific changes to the cloned HSB dependency. Their use
requires compatible FPGA firmware. They are not claims of upstream acceptance
or validation across all HSB reference boards.
