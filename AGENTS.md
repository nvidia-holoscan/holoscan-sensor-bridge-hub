# AGENTS.md

Guidance for AI agents working in the **Holoscan Sensor Bridge Hub** repository (a Holohub-layout repo, part of [Holohub](https://github.com/nvidia-holoscan/holohub)).

## Repository Structure

Projects live under `applications/`, `operators/`, and `tutorials/`. Each project has a `metadata.json` (configuration, modes, dependencies) and a `CMakeLists.txt` where applicable (build registration). Check a project's README for hardware requirements and data downloads before building.

Workflows, benchmarks, GXF extensions, and Debian packages belong in the main [Holohub](https://github.com/nvidia-holoscan/holohub) repository, not here.

## Boundaries

- **Always** run `./holohub run-container -- "./holohub lint --install-dependencies; ./holohub lint"` before committing
- **Always** use `--dryrun --verbose` to inspect a CLI command before running it for real
- **Ask first** before changing `metadata.json` schemas, shared Dockerfiles, or CMake registration macros (`add_holohub_application`, `add_holohub_operator`, etc.)
- **Never** delete `build/`, `data/`, or `install/` directories without asking

## References

- [Main README](README.md) — overview, building, running, contributing
- [Contributing Guide](CONTRIBUTING.md) — how to contribute to this repository
- [Holohub CONTRIBUTING](https://github.com/nvidia-holoscan/holohub/blob/main/CONTRIBUTING.md) — shared conventions and additional component types
- [CLI Reference](utilities/cli/cli_reference.md) — commands, flags, modes, environment variables
- [CLI Developer Guide](utilities/cli/cli_dev_guide.md) — workflow tips, implementation invariants, and extension guide
- [Holoscan SDK User Guide](https://docs.nvidia.com/holoscan/sdk-user-guide/overview.html)
