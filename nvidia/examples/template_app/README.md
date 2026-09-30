# Application Template

Minimal Holoscan application to copy when starting a new example or demo. It sends the integers 1 to 10 from a transmitter operator to a receiver operator that logs each value.

## Overview

To start a new project, copy this folder into your organization's folder, for example to `<org>/<project>/`, rename the `template_app` target, and replace the ping operators in `main.cpp` with your sensor pipeline. Keep every section of this README and fill it in for your project.

For Holoscan Sensor Bridge pipelines to build on, see the HSB [examples](https://github.com/nvidia-holoscan/holoscan-sensor-bridge/tree/main/examples) and the HSB [Applications](https://docs.nvidia.com/holoscan/sensor-bridge/applications/applications) guide.

## Tested Configuration

| Component | Version |
| --- | --- |
| Holoscan SDK | 4.6.0 |
| Operating system | Ubuntu 22.04 (x86_64) |
| Holoscan Sensor Bridge | Not used |
| Developer kit | Not used |

List the exact versions your project was last tested with, including the Holoscan Sensor Bridge release, developer kit, operating system (JetPack, IGX OS, or Ubuntu), FPGA bitstream, and sensor firmware.

## Hardware

None. The ping operators run on the CPU.

## Setup

Install [Holoscan SDK](https://docs.nvidia.com/holoscan/sdk-user-guide/sdk_installation.html) 4.6.0, or build inside the Holoscan SDK container:

```sh
docker run --rm -it --runtime=nvidia --gpus all \
  -v "$(pwd)":/workspace/template_app -w /workspace/template_app \
  nvcr.io/nvidia/clara-holoscan/holoscan:v4.6.0-cuda13
```

Projects that use Holoscan Sensor Bridge usually build and run in the HSB container instead; see the HSB [build guide](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/build).

## Build

From this directory:

```sh
cmake -S . -B build
cmake --build build
```

If Holoscan SDK is not installed in `/opt/nvidia/holoscan`, add `-Dholoscan_DIR=<sdk>/lib/cmake/holoscan` to the first command.

## Run

```sh
./build/template_app
```

## Test

```sh
ctest --test-dir build --output-on-failure
```

The test passes when the receiver logs the tenth value.

## Expected Output

```text
[info] [ping_rx.cpp:25] Rx message value: 1
[info] [ping_rx.cpp:25] Rx message value: 2
...
[info] [ping_rx.cpp:25] Rx message value: 10
```

## Limitations

The template does not use Holoscan Sensor Bridge or any sensor.

## License

Apache License 2.0. See [LICENSE](../../../LICENSE).

## Support

Maintained by the NVIDIA Holoscan Sensor Bridge team. Report issues on the [Holoscan Sensor Bridge Hub issue tracker](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/issues).
