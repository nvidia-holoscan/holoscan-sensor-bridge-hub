# Tools

Opt-in helpers shared by Holoscan Sensor Bridge Hub projects, and the scripts behind the repository's CI checks.

Projects must still build on their own. Referencing a helper here by relative path ties a project to this repository, so copy the helper into your project if it should also build elsewhere.

| Path | Purpose |
| --- | --- |
| [`cmake/`](./cmake/) | CMake modules for Holoscan projects |
| [`docker/`](./docker/) | Optional development image based on the Holoscan SDK container |
| [`lint/`](./lint/) | Lint settings and tool versions used by pre-commit and CI |
| [`metadata/`](./metadata/) | Schemas and checks for optional `metadata.json` files |

## CMake Modules

Add the directory to `CMAKE_MODULE_PATH` in your project's `CMakeLists.txt`, adjusting the relative path to your project's depth, then include the modules you need:

```cmake
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../../../tools/cmake")
include(FetchHolohubOperator)
fetch_holohub_operator(realsense_camera)
```

| Module | Provides |
| --- | --- |
| `FetchHolohubOperator` | `fetch_holohub_operator()` to fetch and build an operator from [Holohub](https://github.com/nvidia-holoscan/holohub) |
| `GenHeaderFromFile` | `gen_header_from_file()` to embed a text or binary file in a C++ header |
| `grpc_generate_cpp`, `grpc_generate_python` | `grpc_generate_cpp()` and `grpc_generate_python()` to generate gRPC code from `.proto` files |
| `nvidia_video_codec` | Finds the NVIDIA Video Codec decode and encode libraries |
| `FindS3DK` | `find_package(S3DK)` |
| `RTIConnextDDS` | `rticodegen()` and `add_rti_type_library()` for RTI Connext DDS types |
| `add_python_tests` | `add_python_tests()` to register pytest tests with CTest |

## Development Image

This image adds common development packages to the Holoscan SDK container. It does not include Holoscan Sensor Bridge; projects that use HSB usually build and run in the HSB container instead, described in the HSB [build guide](https://docs.nvidia.com/holoscan/sensor-bridge/getting-started/build).

Build the image from the repository root, choosing the Holoscan SDK image for your host:

```sh
docker build -f tools/docker/Dockerfile \
  --build-arg BASE_IMAGE=nvcr.io/nvidia/clara-holoscan/holoscan:v4.6.0-cuda13 \
  -t holoscan-sensor-bridge-hub:dev .
```

On hosts with a CUDA 12 driver, use the `v4.6.0-cuda12-dgpu` or `v4.6.0-cuda12-igpu` tag instead. Add `--target aja`, `--target dds`, or `--target yuan-qcap` for the stages with extra dependencies. BuildKit applies `docker/Dockerfile.dockerignore` to this build.

Start a container with the repository mounted:

```sh
docker run --rm -it --runtime=nvidia --gpus all --net host --ipc=host \
  -v "$(pwd)":/workspace/holoscan-sensor-bridge-hub \
  -w /workspace/holoscan-sensor-bridge-hub \
  holoscan-sensor-bridge-hub:dev
```

Projects may need more options, such as device access or display forwarding; see each project's README.

## Metadata Checks

`metadata.json` is optional. When present, it must contain exactly one of the `application`, `operator`, `tutorial`, or `benchmark` keys and match the corresponding schema in [`metadata/`](./metadata/). CI runs these checks from the repository root:

```sh
python3 -m pip install -r tools/metadata/requirements.txt
python3 tools/metadata/metadata_validator.py
python3 tools/metadata/gather_metadata.py
```

`gather_metadata.py` collects every project's metadata into `aggregate_metadata.json`, and `summarize_metadata.py` prints a summary table.

## Linting

```sh
python3 -m pip install -r tools/lint/requirements.txt
pre-commit run --all-files
```

The hooks in `.pre-commit-config.yaml` read their settings from `lint/`:

| File | Used by |
| --- | --- |
| [`pyproject.toml`](./lint/pyproject.toml) | black, isort, ruff, and codespell |
| [`.markdownlint.yaml`](./lint/.markdownlint.yaml) | markdownlint |
| [`codespell_ignore_words.txt`](./lint/codespell_ignore_words.txt) | codespell |
| [`.clang-format`](./lint/.clang-format) | clang-format (not run by the hooks) |

cpplint settings are passed as hook arguments. To use the same settings in an editor or when running a tool directly, point it at these files, for example `black --config tools/lint/pyproject.toml` or `clang-format --style=file:tools/lint/.clang-format`.
