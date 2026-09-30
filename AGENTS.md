# AGENTS.md

Guidance for AI agents working in the **Holoscan Sensor Bridge Hub** repository.

## Repository Structure

Projects live in the folder of the organization that maintains them, either directly (`<org>/<project>/`) or in an optional category folder (for example, `nvidia/operators/<project>/`). Suggested categories are `operators`, `examples`, `demos`, `fpga`, `ai/skills`, `benchmarks`, `tutorials`, and `utilities`. Create organization and category folders only when adding their first project, and start new projects from `nvidia/examples/template_app/` or `nvidia/operators/template_op/`.

Projects build on [Holoscan Sensor Bridge](https://github.com/nvidia-holoscan/holoscan-sensor-bridge) (HSB). Changes to HSB itself (host software, operators, FPGA IP, firmware, emulator) belong in the HSB repository, not here.

Each project builds on its own and documents its hardware, tested versions (including the HSB release), and build, run, and test commands in its `README.md`; `metadata.json` is optional. Shared, opt-in helpers (CMake modules, a development Dockerfile, metadata schemas and checks) and the lint settings live in `tools/`; only `.gitignore` and `.pre-commit-config.yaml` stay at the repository root.

## Boundaries

- **Always** run `pre-commit run --all-files` before committing (install the tools with `python3 -m pip install -r tools/lint/requirements.txt`)
- **Always** sign off commits (`git commit -s`)
- **Ask first** before adding repository-wide build systems, containers, or CLIs, before changing the shared helpers or metadata schemas in `tools/`, or before making one project depend on another
- **Ask first** before copying HSB source into a project; build against a tagged HSB release instead, and keep any HSB changes as patches against it
- **Never** delete `build/`, `data/`, or `install/` directories without asking

## References

- [Main README](README.md) — repository organization and linting
- [Contributing Guide](CONTRIBUTING.md) — project requirements, ownership, and review
- [Tools](tools/README.md) — shared helpers and CI checks
- [Holoscan Sensor Bridge repository](https://github.com/nvidia-holoscan/holoscan-sensor-bridge) and [user guide](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/introduction)
- [Holoscan SDK User Guide](https://docs.nvidia.com/holoscan/sdk-user-guide/overview.html)
