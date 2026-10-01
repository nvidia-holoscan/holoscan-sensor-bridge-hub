# Analog Devices Sensor Enablement for NVIDIA Holoscan Sensor Bridge

This directory contains **Analog Devices (ADI)** sensor integrations, GPU-accelerated operators, Python bindings, ROS 2 applications, and reference pipelines for the **NVIDIA Holoscan Sensor Bridge** ecosystem.

These examples demonstrate how ADI sensing technologies can be integrated into NVIDIA Holoscan workflows for real-time robotics, industrial automation, edge AI, autonomous systems, and multi-modal sensor fusion.

Current support includes:

- **3D depth sensing** using the **ADCAM3175-2M-EBZ** Time-of-Flight camera
- **Industrial IMUs** including **ADIS16505** and **ADIS16607**
- **Spatial audio processing** using **A2B (AD2428/AD2427)** microphone systems
- **ROS 2 integration**
- **GPU-accelerated sensor processing**
- **Holoviz visualization**

## Table of Contents

- [Supported Hardware](#supported-hardware)
- [Repository Layout](#repository-layout)
- [Module Documentation](#module-documentation)
- [Prerequisites](#prerequisites)
- [Build](#build)
- [ADCAM3175-2M-EBZ Time-of-Flight Camera](#module-1--adcam3175-2m-ebz-time-of-flight-camera)
- [Industrial IMU Integration](#module-2--industrial-imu-integration)
- [A2B Audio Processing Pipeline](#module-3--a2b-audio-processing-pipeline)
- [ROS 2 Integration](#ros-2-integration)
- [Technology Stack](#technology-stack)
- [Multi-Modal Sensor Fusion](#multi-modal-sensor-fusion)
- [License](#license)
- [Support](#support)

## Supported Hardware

| Category | Part Number / Platform | Status | Description | Product Link |
| --- | --- | --- | --- | --- |
| 3D Depth Camera | ADCAM3175-2M-EBZ / ADTF3175 | Supported | Time-of-Flight 3D depth camera | [ADTF3175 product page](https://www.analog.com/en/products/adtf3175.html) |
| Industrial IMU | ADIS16505 | Supported | Precision industrial inertial measurement unit | [ADIS16505 product page](https://www.analog.com/en/products/adis16505.html) |
| Industrial IMU | ADIS16607 | Supported | Precision miniature MEMS inertial measurement unit | [ADIS16607 product page](https://www.analog.com/en/products/adis16607.html) |
| A2B Audio | AD2428 | Supported | A2B transceiver used for the master node | [AD2428 product page](https://www.analog.com/en/products/ad2428.html) |
| A2B Audio | AD2427 | Supported | A2B transceiver used for microphone nodes | [AD2427 product page](https://www.analog.com/en/products/ad2427.html) |
| Sensor Connectivity | NVIDIA Holoscan Sensor Bridge | Supported | FPGA-based sensor connectivity platform | [Holoscan Sensor Bridge repository](https://github.com/nvidia-holoscan/holoscan-sensor-bridge) |
| AI Compute | NVIDIA Jetson / IGX / DGX Spark | Supported | GPU-accelerated AI processing platforms | [NVIDIA Holoscan product page](https://www.nvidia.com/en-us/clara/holoscan/) |

## Repository Layout

The ADI sensor package is organized into three primary sensor domains:

- [`aditof`](aditof/README.md): ADCAM3175-2M-EBZ Time-of-Flight camera support
- [`adi_imu`](adi_imu/README.md): ADIS16505 and ADIS16607 IMU support
- [`a2baudio`](a2baudio/README.md): A2B microphone acquisition, beamforming, DSP, and visualization

```text
adi/
└── adi_sensors/
    ├── README.md
    ├── requirements.txt
    ├── Dockerfile
    ├── CMakeLists.txt
    ├── prepare_hsb.py
    ├── code_README.md
    ├── smoke_test.py
    ├── metadata.json
    ├── patches/
    │   └── 0001-adi-spi-gpio.patch
    ├── aditof/
    │   ├── README.md
    │   ├── CMakeLists.txt
    │   ├── adi_manifest.yaml
    │   ├── python/
    │   │   ├── adcam.py
    │   │   └── adcam_player.py
    │   └── cpp/
    │       ├── CMakeLists.txt
    │       ├── adcam_player.cpp
    │       ├── adcam_lib.hpp
    │       ├── adcam_lib.cpp
    │       ├── adcam_calibration.hpp
    │       ├── adcam_calibration.cpp
    │       ├── adcam_unpack_op.hpp
    │       ├── adcam_unpack_op.cpp
    │       ├── adcam_unpack_op.cu
    │       ├── programmer.hpp
    │       ├── programmer.cpp
    │       ├── adsd3500_flash.hpp
    │       ├── adsd3500_flash.cpp
    │       ├── compute_crc.hpp
    │       ├── compute_crc.cpp
    │       └── crc_table.cpp
    ├── adi_imu/
    │   ├── README.md
    │   ├── CPPLINT.cfg
    │   ├── CMakeLists.txt
    │   ├── adi_imu_op.hpp
    │   ├── adi_imu_op.cpp
    │   ├── app/
    │   │   ├── adi_imu_config.yaml
    │   │   ├── adi_imu_config2.yaml
    │   │   ├── adi_imu_ros2.py
    │   │   ├── adi_imu_visualization.launch.py
    │   │   ├── config.xml
    │   │   ├── ros_setup.sh
    │   │   └── packed_frame.bin
    │   └── python/
    │       ├── __init__.py
    │       ├── adi_imu_op_python.cpp
    │       └── adi_imu_op_pydoc.hpp
    └── a2baudio/
        ├── README.md
        ├── CMakeLists.txt
        ├── app/
        │   ├── CMakeLists.txt
        │   └── audio_viz.cpp
        ├── i2s/
        │   ├── CMakeLists.txt
        │   ├── i2s_receiver_op.hpp
        │   └── i2s_receiver_op.cpp
        ├── audio_waveform/
        │   ├── CMakeLists.txt
        │   ├── audio_waveform_op.hpp
        │   └── audio_waveform_op.cu
        ├── audio_beamformer/
        │   ├── CMakeLists.txt
        │   ├── audio_beamformer_op.hpp
        │   ├── audio_beamformer_op.cpp
        │   └── audio_beamformer_op.cu
        └── audio_filewriter/
            ├── CMakeLists.txt
            ├── audio_file_writer_op.hpp
            └── audio_file_writer_op.cpp
```

## Module Documentation

| Module | Documentation | Description |
| --- | --- | --- |
| ADCAM3175 ToF Camera | [`aditof/README.md`](aditof/README.md) | Camera control, frame capture, CUDA unpacking, visualization, calibration, and firmware management |
| ADI IMU | [`adi_imu/README.md`](adi_imu/README.md) | IMU acquisition, Python bindings, ROS 2 publishing, and visualization |
| A2B Audio | [`a2baudio/README.md`](a2baudio/README.md) | I2S reception, waveform generation, beamforming, recording, and Holoviz visualization |

## Prerequisites

### Hardware

- NVIDIA Jetson, IGX, or supported discrete-GPU system
- NVIDIA Holoscan Sensor Bridge
- One or more supported ADI sensors
- Compatible network interface for the selected Sensor Bridge data path

### Software

- NVIDIA GPU driver appropriate for the target platform
- Docker
- NVIDIA Container Toolkit
- Access to the Holoscan SDK container image used by the build
- CMake and the compiler toolchain supplied by the container
- Python dependencies listed in `adi/adi_sensors/requirements.txt`
- ROS 2 Humble or Jazzy for IMU ROS 2 workflows

## Build

Run all host-side commands from the root of the Holoscan Sensor Bridge repository.

### 1. Build the Docker Image

```bash
docker build \
  -f adi/adi_sensors/Dockerfile \
  --build-arg BASE_IMAGE=nvcr.io/nvidia/clara-holoscan/holoscan:v4.6.0-cuda13 \
  -t hsb-adi:2.7.0 .
```

### 2. Allow X11 Access for GUI Applications

Holoviz applications require access to the host display:

```bash
xhost +
```

### 3. Run the Development Container

```bash
docker run --rm -it \
  --runtime=nvidia \
  --gpus all \
  --net host \
  --ipc=host \
  --ulimit stack=67108864 \
  -e NVIDIA_DRIVER_CAPABILITIES=graphics,video,compute,utility,display \
  -e NVIDIA_VISIBLE_DEVICES=all \
  -e DISPLAY="$DISPLAY" \
  -v "$(pwd)":/workspace/holoscan-sensor-bridge-hub \
  -w /workspace/holoscan-sensor-bridge-hub \
  hsb-adi:2.7.0
```

### 4. Configure the Build Inside the Container

Docker build will genenrate all executables. They should be already in path. To build separately, you can use below steps. Ensure step 3 has been executed first.

```bash
export LD_LIBRARY_PATH=/opt/nvidia/holoscan/lib:${LD_LIBRARY_PATH}
cd adi/adi_sensors
cmake -S . -B build
```

### 5. Build All Enabled Targets

```bash
cmake --build build -j"$(nproc)"
```

To build a specific target, use:

```bash
cmake --build build --target <target-name> -j"$(nproc)"
```

### 6. Run the Smoke Test

```bash
python3 adi/adi_sensors/smoke_test.py
```

## Module 1 – ADCAM3175-2M-EBZ Time-of-Flight Camera

Directory: [`aditof/`](aditof/)

### ADCAM3175-2M-EBZ Time-of-Flight Camera Overview

This module enables the **ADCAM3175-2M-EBZ** ToF camera within NVIDIA Holoscan.

Features include:

- Camera discovery and configuration
- Device control APIs
- Calibration support
- Frame capture
- CUDA-based frame unpacking
- Playback and visualization utilities
- Firmware management
- Sensor Bridge integration

Typical applications include spatial perception, robot navigation, obstacle detection, human-machine interaction, industrial inspection, SLAM, and 3D reconstruction.

### ADCAM3175-2M-EBZ Time-of-Flight Camera Key Components

| Component | Description |
| --- | --- |
| `adcam_lib` | Camera control library |
| `adcam_unpack_op` | GPU-accelerated depth frame unpacking |
| `adcam_player` | C++ and Python reference player |
| `adcam_calibration` | Camera calibration support |
| `adsd3500_flash` | Firmware flashing support |
| `programmer` | Device programming utilities |

### Example

```bash
python3 adi/adi_sensors/aditof/python/adcam_player.py
```

For detailed options and firmware procedures, see [`aditof/README.md`](aditof/README.md).

## Module 2 – Industrial IMU Integration

Directory: [`adi_imu/`](adi_imu/)

### Supported Devices

| Device | Status | Product Link |
| --- | --- | --- |
| ADIS16505 | Supported | [ADIS16505 product page](https://www.analog.com/en/products/adis16505.html) |
| ADIS16607 | Supported | [ADIS16607 product page](https://www.analog.com/en/products/adis16607.html) |

### Industrial IMU Integration Overview

This module integrates ADI industrial IMUs into NVIDIA Holoscan pipelines.

Features include:

- IMU acquisition
- Python bindings
- Holoscan operators
- ROS 2 publishing
- Visualization support
- Timestamp synchronization

Measurements include accelerometer data, gyroscope data, temperature, and sensor timestamps.

### Architecture

```text
ADIS16505 / ADIS16607
          │
          ▼
    Sensor Bridge
          │
          ▼
      Holoscan
          │
    ┌─────┴─────┐
    ▼           ▼
Processing    ROS 2
    │           │
    ▼           ▼
 Holoviz       RViz
```

### Key Components

| Component | Description |
| --- | --- |
| `adi_imu_op` | IMU acquisition operator |
| `adi_imu_ros2.py` | ROS 2 publisher application |
| `adi_imu_op_python` | Python bindings |
| `adi_imu_visualization.launch.py` | RViz visualization launch file |

### Examples

Run the IMU ROS 2 application:

```bash
python3 adi/adi_sensors/adi_imu/app/adi_imu_ros2.py
```

Run RViz visualization in a separate shell with the ROS 2 environment sourced:

```bash
ros2 launch adi/adi_sensors/adi_imu/app/adi_imu_visualization.launch.py
```

Typical use cases include visual-inertial odometry, robot localization, navigation, humanoid robotics, sensor fusion, and autonomous mobile robots.

For detailed setup and configuration, see [`adi_imu/README.md`](adi_imu/README.md).

## Module 3 – A2B Audio Processing Pipeline

Directory: [`a2baudio/`](a2baudio/)

### A2B Audio Processing Pipeline Overview

This module demonstrates an A2B microphone acquisition and processing pipeline using Holoscan Sensor Bridge and NVIDIA GPUs.

```text
AD2428 A2B Master
         │
         ▼
AD2427 Microphone Node
         │
         ▼
 4-Microphone Array
         │
         ▼
 Holoscan Sensor Bridge
         │
         ▼
 NVIDIA GPU
```

Features include:

- Multi-channel microphone capture
- I2S audio reception
- Real-time waveform rendering
- FFT visualization
- Digital beamforming
- Audio recording
- CUDA acceleration
- Holoviz integration

### Components

| Component | Directory | Description |
| --- | --- | --- |
| I2S Receiver | `i2s/` | Receives audio streams from the Sensor Bridge |
| Audio Waveform | `audio_waveform/` | Generates waveform data for real-time visualization |
| Audio Beamformer | `audio_beamformer/` | Performs GPU-accelerated multi-channel beamforming |
| Audio File Writer | `audio_filewriter/` | Stores captured audio streams to disk |
| Visualization Application | `app/` | Connects acquisition, DSP, beamforming, FFT, and Holoviz rendering |

Typical applications include voice-controlled robots, human-robot interaction, industrial acoustic monitoring, sound-source localization, spatial audio, and voice analytics.

For detailed setup and usage, see [`a2baudio/README.md`](a2baudio/README.md).

## ROS 2 Integration

ROS 2 support is provided primarily through the IMU workflow.

Included components:

```text
adi_imu/app/adi_imu_ros2.py
adi_imu/app/adi_imu_visualization.launch.py
adi_imu/app/config.xml
adi_imu/app/ros_setup.sh
```

Capabilities include:

- Sensor publishers
- ROS 2 message support
- Cyclone DDS configuration
- RViz visualization
- Sensor-fusion integration

## Technology Stack

- NVIDIA Holoscan
- NVIDIA Holoscan Sensor Bridge
- CUDA
- C++
- Python
- ROS 2
- Holoviz
- RViz
- A2B Audio
- Industrial IMUs
- Time-of-Flight depth sensing

## Multi-Modal Sensor Fusion

These modules demonstrate how multiple sensing modalities can be combined within a unified Holoscan pipeline:

```text
3D Depth Camera ─┐
                 │
Industrial IMU ──┼──► Holoscan ──► GPU Processing ──► AI / Visualization
                 │
A2B Audio ───────┘
```

Applications include:

- Autonomous mobile robots
- Humanoid robotics
- Industrial automation
- Spatial AI
- Edge AI
- Intelligent perception systems

Together, ADI sensing technologies and NVIDIA accelerated computing provide a scalable foundation for robotics and physical AI platforms.

## License

Refer to the main repository license and contribution guidelines for usage restrictions and contribution policies.

## Support

- Contact the applicable FPGA vendor for access to Sensor Bridge RTL supporting ADI modules.
- Contact **<Holo.Scan@analog.com>** for ADI Holoscan support inquiries.
