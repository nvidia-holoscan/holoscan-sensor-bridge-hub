# Holoscan Sensor Bridge Hub — Applications

Applications for the Holoscan platform, as part of [Holoscan Sensor Bridge Hub](../README.md) (a Holohub sub-catalog).

This directory contains applications based on the Holoscan Platform.
Some applications might require specific hardware and software packages which are described in the
metadata.json and/or README.md for each application.

## Contributing to HoloHub Applications

Please review the [CONTRIBUTING.md file](https://github.com/nvidia-holoscan/holohub/blob/main/CONTRIBUTING.md) guidelines to contribute applications.

## HoloHub Application Organization Conventions

## Starting a New Project

From the repository root, generate an application from the [application template](./template/):

```sh
./hsb create my_app --language cpp -i false --dryrun
./hsb create my_app --language cpp -i false
```

Use `--language python` for a Python application. The wrapper installs the CLI's
creation dependencies automatically, and `create` validates the generated metadata and
registers the app in `applications/CMakeLists.txt`. Omit `-i false` for interactive
prompts. The same commands work inside the development container.

Use `--template <directory>` to choose another Cookiecutter template, or set
`HOLOSCAN_CLI_CREATE_TEMPLATE` to change the default. The operator and tutorial
`template/` folders currently contain documentation stubs for manual copying;
`applications/template` provides the executable C++ and Python scaffolds.

Build and run the generated app from the repository root:

```sh
./hsb build my_app --dryrun --verbose
./hsb build my_app
./hsb run my_app --dryrun --verbose
./hsb run my_app
```

## Required Conventions

We expect that an application contributed to HoloHub conforms to the following organization:

- Each project must provide a `metadata.json` file reflecting several key components such as the application name and description, authors, dependencies, and the primary project language.
- Each project must provide a `README` or `README.md` file.
  - We strongly recommend that the project `README` file provides at least the information given in the [template README](./template/README.md.template), including the project description and a splash image.
- Each project must be organized in its own subfolder under `applications/`.

See the [HoloHub application template](./template/) for example `README` and `metadata.json` documents to get started.

## Recommended Conventions

Contributors may additionally opt to lay out their project structure in a way that conforms to HoloHub conventions in order to enable common infrastructure for their project.

HoloHub recommended application convention is as follows:

- Languages
  - Project is either C++ or Python language
  - If multiple language implementations are provided, each must be added to its own language subfolder as follows:

```text
applications/
  └── my_project/
        ├── cpp/
        │     ├── ...
        │     └── ...
        └── python/
              ├── ...
              └── ...
```

- Container Environment
  - Project may provide its own container environment or opt to use the default HoloHub environment
  - If the project specifies its own container:
    - Default project environment must be named `Dockerfile`
    - Project `Dockerfile` must be located at either:
      - The same directory as `metadata.json`, or
      - The project may provide an alternative default Dockerfile path in `metadata.json`
  - If the project does not specify a `Dockerfile` then the [default `Dockerfile`](../Dockerfile) will be used

- Build and Run Instructions
  - Must provide a run command in `metadata.json`
  - Advanced instructions may also be specified in the project README
