# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""Prepare a pinned HSB checkout with ADI hardware patches, without resetting files."""

import argparse
import subprocess
from pathlib import Path

HSB_REPOSITORY = "https://github.com/nvidia-holoscan/holoscan-sensor-bridge.git"
HSB_TAG = "2.7.0"
HSB_COMMIT = "1df133d4c78a6921249be4b147d65554aa8efa68"


def prepare(destination):
    destination = destination.resolve()
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth=1", "--branch", HSB_TAG, HSB_REPOSITORY, str(destination)],
            check=True,
        )
    if not (destination / ".git").exists():
        raise RuntimeError(f"{destination} already exists and is not an HSB Git checkout")
    revision = subprocess.check_output(
        ["git", "-C", str(destination), "rev-parse", "HEAD"], text=True
    ).strip()
    if revision != HSB_COMMIT:
        raise RuntimeError(
            f"Expected HSB {HSB_TAG} ({HSB_COMMIT}), found {revision}; no files changed"
        )
    patch = Path(__file__).parent / "patches" / "0001-adi-spi-gpio.patch"
    command = ["git", "-C", str(destination), "apply"]
    already_applied = subprocess.run(
        [*command, "--reverse", "--check", str(patch)], capture_output=True
    )
    if already_applied.returncode == 0:
        print(f"ADI hardware patches are already applied in {destination}")
        return
    subprocess.run([*command, "--check", str(patch)], check=True)
    subprocess.run([*command, str(patch)], check=True)
    print(f"Prepared HSB {HSB_TAG} with ADI hardware patches in {destination}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "destination", type=Path, help="New directory or existing HSB 2.7.0 checkout"
    )
    args = parser.parse_args()
    try:
        prepare(args.destination)
    except (RuntimeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
