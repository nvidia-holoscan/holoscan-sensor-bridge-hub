# AGENTS.md

Guidance for AI agents working in the **Holoscan Sensor Bridge Hub** repository (a Holohub-layout repo, part of [Holohub](https://github.com/nvidia-holoscan/holohub)).

## Repository Structure

Projects live under `applications/`, `operators/`, and `tutorials/`. Each project has a `metadata.json` (configuration, modes, dependencies) and a `CMakeLists.txt` where applicable (build registration). Check a project's README for hardware requirements and data downloads before building.

Workflows, benchmarks, GXF extensions, and Debian packages belong in the main [Holohub](https://github.com/nvidia-holoscan/holohub) repository, not here.

## Boundaries

- **Always** run `./hsb run-container -- "./hsb lint --install-dependencies; ./hsb lint"` before committing
- **Always** use `--dryrun --verbose` to inspect a CLI command before running it for real, where those flags are supported
- **Ask first** before changing `metadata.json` schemas, shared Dockerfiles, or CMake registration macros (`add_holohub_application`, `add_holohub_operator`, etc.)
- **Never** delete `build/`, `data/`, or `install/` directories without asking

## References

- [Main README](README.md) — overview, building, running, contributing
- [Contributing Guide](CONTRIBUTING.md) — how to contribute to this repository
- [Holohub CONTRIBUTING](https://github.com/nvidia-holoscan/holohub/blob/main/CONTRIBUTING.md) — shared conventions and additional component types
- [Developer Guide](doc/developer.md) — container and native build workflows
- [Holoscan SDK User Guide](https://docs.nvidia.com/holoscan/sdk-user-guide/overview.html)
