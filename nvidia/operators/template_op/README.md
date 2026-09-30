# Template Operator

Minimal Holoscan operator to copy when starting a new operator. `TemplateOp` multiplies each integer it receives by its `multiplier` parameter and emits the result.

## Overview

To start a new operator, copy this folder to `<org>/operators/<project>/`, rename `TemplateOp` and the `template_op` files and targets, and replace the logic in `template_op.cpp`. Keep every section of this README and fill it in for your project.

| Port or parameter | Type | Description |
| --- | --- | --- |
| `in` (input) | `int` | Value to multiply |
| `out` (output) | `int` | Input value multiplied by `multiplier` |
| `multiplier` (parameter) | `int` | Factor applied to each input value (default: `2`) |

`test_template_op.cpp` connects the operator between the Holoscan SDK ping transmitter and receiver, and serves as the operator's test.

To support a new sensor with Holoscan Sensor Bridge, see the HSB [New Sensors](https://docs.nvidia.com/holoscan/sensor-bridge/applications/new-sensors) guide and the HSB [examples](https://github.com/nvidia-holoscan/holoscan-sensor-bridge/tree/main/examples).

## Tested Configuration

| Component | Version |
| --- | --- |
| Holoscan SDK | 4.6.0 |
| Operating system | Ubuntu 22.04 (x86_64) |
| Holoscan Sensor Bridge | Not used |
| Developer kit | Not used |

List the exact versions your project was last tested with, including the Holoscan Sensor Bridge release, developer kit, operating system (JetPack, IGX OS, or Ubuntu), FPGA bitstream, and sensor firmware.

## Hardware

None. The operator runs on the CPU.

## Setup

Install [Holoscan SDK](https://docs.nvidia.com/holoscan/sdk-user-guide/sdk_installation.html) 4.6.0, or build inside the Holoscan SDK container:

```sh
docker run --rm -it --runtime=nvidia --gpus all \
  -v "$(pwd)":/workspace/template_op -w /workspace/template_op \
  nvcr.io/nvidia/clara-holoscan/holoscan:v4.6.0-cuda13
```

Projects that use Holoscan Sensor Bridge usually build and run in the HSB container instead; see the HSB [build guide](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/build).

## Build

From this directory:

```sh
cmake -S . -B build
cmake --build build
```

This builds the `template_op` library and the `test_template_op` application. If Holoscan SDK is not installed in `/opt/nvidia/holoscan`, add `-Dholoscan_DIR=<sdk>/lib/cmake/holoscan` to the first command.

## Run

```sh
./build/test_template_op
```

## Test

```sh
ctest --test-dir build --output-on-failure
```

The test sends 1, 2, and 3 through the operator with a multiplier of 2, and passes when the receiver logs 6.

## Expected Output

```text
[info] [ping_rx.cpp:25] Rx message value: 2
[info] [ping_rx.cpp:25] Rx message value: 4
[info] [ping_rx.cpp:25] Rx message value: 6
```

## Limitations

The template does not use Holoscan Sensor Bridge or any sensor, and has no Python bindings.

## License

Apache License 2.0. See [LICENSE](../../../LICENSE).

## Support

Maintained by the NVIDIA Holoscan Sensor Bridge team. Report issues on the [Holoscan Sensor Bridge Hub issue tracker](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/issues).
