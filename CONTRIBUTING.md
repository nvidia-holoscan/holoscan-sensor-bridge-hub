# Contributing to Holoscan Sensor Bridge Hub

Holoscan Sensor Bridge Hub is a curated collection of integrations and sensor demos for [Holoscan Sensor Bridge](https://github.com/nvidia-holoscan/holoscan-sensor-bridge) (HSB) from NVIDIA and ecosystem partners. NVIDIA maintainers decide which contributions to accept, and contributors maintain the projects they add.

## Table of Contents

- [What Belongs Here](#what-belongs-here)
- [Repository Organization](#repository-organization)
- [Project Requirements](#project-requirements)
- [Building on Holoscan Sensor Bridge](#building-on-holoscan-sensor-bridge)
- [Ownership and Review](#ownership-and-review)
- [Developer Process](#developer-process)
- [Code Quality](#code-quality)
- [Signing Your Work](#signing-your-work)
- [Reporting Issues](#reporting-issues)

## What Belongs Here

This repository accepts reusable HSB integrations and sensor demos. Complete end-to-end Holoscan applications that are not centered on HSB belong in other Holoscan repositories, such as [Holohub](https://github.com/nvidia-holoscan/holohub).

Changes to HSB itself, such as its host software, operators, FPGA IP, firmware, or emulator, belong in the [HSB repository](https://github.com/nvidia-holoscan/holoscan-sensor-bridge); see its [contributing guide](https://github.com/nvidia-holoscan/holoscan-sensor-bridge/blob/main/CONTRIBUTING.md).

Maintainers may decline a contribution based on scope, duplication, quality, dependencies, or missing ownership.

## Repository Organization

Place each project in the folder of the organization that maintains it, such as `nvidia/`, `adi/`, or `altera/`. Inside that folder, a project can sit directly in `<org>/<project>/` or in an optional category folder, such as `<org>/operators/<project>/`. Suggested categories:

| Category | Contents |
| --- | --- |
| `operators` | Reusable Holoscan operators |
| `examples` | Example applications |
| `demos` | Sensor and system demos |
| `fpga` | FPGA designs, one folder per platform |
| `ai/skills` | AI agent skills |
| `benchmarks` | Benchmarks |
| `tutorials` | Tutorials and how-to guides |
| `utilities` | Utilities and tools |

- Create organization and category folders only when you add their first project.
- Each project has one primary owner, who may differ from the hardware vendor.
- Shared, opt-in helpers live in [`tools/`](./tools/README.md).

## Project Requirements

Start from the [application template](./nvidia/examples/template_app/) or the [operator template](./nvidia/operators/template_op/). Every project must meet these requirements:

- **Builds independently**: The project has its own build files, such as `CMakeLists.txt`, a `Dockerfile`, or `requirements.txt`, and does not depend on other projects in this repository.
- **Uses an HSB release**: The project builds against a tagged [HSB release](https://github.com/nvidia-holoscan/holoscan-sensor-bridge/releases), for example inside the HSB container, rather than a copy of the HSB source. If it needs changes to HSB, keep them as patches against that release and describe them in the README.
- **README**: The project's `README.md` covers its purpose, hardware, tested configuration, setup, build, run, and test commands, expected output, limitations, license, and support contact. The templates show each section.
- **Tested configuration**: The README states the exact versions the project was last tested with, including the HSB release, Holoscan SDK, the developer kit, the operating system (JetPack, IGX OS, or Ubuntu), the FPGA bitstream, and sensor firmware.
- **License**: Contributions are licensed under the Apache License 2.0. Contributors may retain copyright. Start each source file with an SPDX header, for example:

  ```text
  SPDX-FileCopyrightText: Copyright (c) 2026, Your Organization. All rights reserved.
  SPDX-License-Identifier: Apache-2.0
  ```

- **Sign-off**: Every commit is [signed off](#signing-your-work).

A `metadata.json` file is optional. If you add one, it must use exactly one of the `application`, `operator`, `tutorial`, or `benchmark` keys and match the corresponding schema in [`tools/metadata/`](./tools/metadata/). CI validates it; see [Metadata Checks](./tools/README.md#metadata-checks).

### License and Legal Guidelines

- **Open Source Compatibility**: Ensure you have rights to contribute your work
- **License Compliance**: All contributions inherit the Apache 2.0 license
- **Patent Considerations**: Verify no patent conflicts are introduced
- **Contribution Signing**: All commits must be signed-off (see [signing requirements](#signing-your-work))

> **Note**: NVIDIA is not responsible for conflicts resulting from community contributions.

## Building on Holoscan Sensor Bridge

The HSB repository and [user guide](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/introduction) cover most of what an integration needs:

- **Setup**: [Hardware setup](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/hardware-setup), [host setup](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/host-setup), [firmware setup](https://docs.nvidia.com/holoscan/sensor-bridge/firmware/firmware-setup), and [building the HSB container](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/build), which most projects build and run in.
- **Applications**: The HSB [examples](https://github.com/nvidia-holoscan/holoscan-sensor-bridge/tree/main/examples) and the [Applications](https://docs.nvidia.com/holoscan/sensor-bridge/applications/applications) guide show complete sensor pipelines in Python and C++.
- **New sensors**: The [New Sensors](https://docs.nvidia.com/holoscan/sensor-bridge/applications/new-sensors) guide and the Hololink module [application](https://docs.nvidia.com/holoscan/sensor-bridge/applications/hololink-module-application-tutorial) and [device driver](https://docs.nvidia.com/holoscan/sensor-bridge/applications/hololink-module-device-driver-tutorial) tutorials explain how to add a sensor.
- **Testing without hardware**: The [HSB emulator](https://docs.nvidia.com/holoscan/sensor-bridge/emulation/hsb-emulator) exercises HSB operators without a sensor bridge board.
- **AI skills**: The HSB [agent skills](https://github.com/nvidia-holoscan/holoscan-sensor-bridge/tree/main/skills) are examples for the `ai/skills` category.
- **Release changes**: Check the HSB [release notes](https://docs.nvidia.com/holoscan/sensor-bridge/support/release-notes) when moving a project to a newer HSB release.

## Ownership and Review

- Contributors maintain their projects and respond to user reports about them.
- Maintainers mark inactive projects as unmaintained, and may de-list or archive them.
- Hosting a project here does not imply NVIDIA certification or maintenance.
- Every pull request needs approval from an NVIDIA maintainer. The project's contributor reviews technical changes to it.
- CI runs basic checks only: linting, copyright headers and internal artifacts, links, and `metadata.json` validation. CI does not build or test contributed projects; contributors test them on the hardware listed in their README.

## Developer Process

1. **Fork the Repository**

   [Fork](https://help.github.com/en/articles/fork-a-repo) the [upstream Holoscan Sensor Bridge Hub repository](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub).

2. **Clone and Set Up Local Development**

   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_FORK.git holoscan-sensor-bridge-hub
   cd holoscan-sensor-bridge-hub

   # Add upstream remote for staying in sync
   git remote add upstream https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub.git

   # Create a feature branch
   git checkout -b feature/your-feature-name
   ```

3. **Develop Your Contribution**

   - Copy a template into your organization's folder, for example to `<org>/<project>/`
   - Meet the [project requirements](#project-requirements)
   - Build and test the project on the configuration listed in its README

4. **Lint, Commit, and Push**

   ```bash
   # Run the lint checks
   pre-commit run --all-files

   # Commit with sign-off (required)
   git add <org>/<project>
   git commit -s -m "Add your descriptive commit message"

   # Push to your fork
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**

   - [Create a Pull Request](https://help.github.com/en/articles/creating-a-pull-request) from your branch to the upstream `main` branch
   - Describe the contribution, its tested configuration, and who maintains it

6. **Review Process**

   - NVIDIA maintainers will review your PR
   - Address any feedback or requested changes
   - Once approved, your contribution will be merged

Thanks in advance for your patience as we review your contributions. We do appreciate them!

## Code Quality

### Linting

Install the lint tools and run all checks from the repository root:

```bash
python3 -m pip install -r tools/lint/requirements.txt
pre-commit run --all-files
```

Many hooks fix issues in place. Rerun `pre-commit run --all-files` until it passes.

### Coding Guidelines

- **Style Compliance**: All code must adhere to Holoscan SDK coding standards
- **Descriptive Naming**: Use clear, English descriptive names for functionality
- **Avoid Abbreviations**: Minimize use of acronyms, brand names, or team names
- **Code Documentation**: Include inline comments for complex logic
- **Error Handling**: Implement appropriate error handling and validation

## Signing Your Work

- We require that all contributors "sign-off" on their commits. This certifies that the contribution is your original work, or you have rights to submit it under the same license, or a compatible license.

  - Any contribution which contains commits that are not Signed-Off will not be accepted.

- To sign off on a commit you simply use the `--signoff` (or `-s`) option when committing your changes:

  ```bash
  git commit -s -m "Add cool feature."
  ```

  This will append the following to your commit message:

  ```text
  Signed-off-by: Your Name <your@email.com>
  ```

- Full text of the DCO (<https://developercertificate.org/>):

  ```text
    Developer Certificate of Origin
    Version 1.1

    Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

    Everyone is permitted to copy and distribute verbatim copies of this
    license document, but changing it is not allowed.


    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.
  ```

> **Important**: Contributions without proper sign-off will not be accepted.

## Reporting Issues

Report bugs and feature requests for a project in this repository on [GitHub Issues](https://github.com/nvidia-holoscan/holoscan-sensor-bridge-hub/issues). Name the project, and mention the maintainer listed in its README. Report problems in HSB itself on the [HSB issue tracker](https://github.com/nvidia-holoscan/holoscan-sensor-bridge/issues).

**When reporting issues, include:**

- Clear description of the problem or enhancement request
- Steps to reproduce (for bugs)
- Expected vs. actual behavior
- Configuration: HSB release, Holoscan SDK, developer kit, and operating system versions
- Relevant logs or error messages
