# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Check the installed ADI executables and Python bindings without contacting a sensor."""

import subprocess
import sys
from pathlib import Path

import hololink
from hololink.operators.adi_imu import create_imu_operator


def main():
    for executable in ("adcam_player", "audio_viz_disp"):
        result = subprocess.run([executable, "--help"], capture_output=True, text=True, check=True)
        if "--hololink" not in result.stdout + result.stderr:
            raise RuntimeError(f"Unexpected help output from {executable}")
        print(f"PASS: {executable} --help")
    player = Path(__file__).parent / "aditof" / "python" / "adcam_player.py"
    subprocess.run([sys.executable, str(player), "--help"], capture_output=True, check=True)
    print("PASS: ToF Python player --help")
    assert hololink.DataChannel is not None
    assert callable(create_imu_operator)
    print("PASS: Hololink and ADI IMU Python bindings import")
    print("Sensor acquisition and ROS2 integration require the corresponding hardware/runtime.")


if __name__ == "__main__":
    main()
