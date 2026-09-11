# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Overview

This application is built using Holoscan SDK version {{ cookiecutter.holoscan_version }} and supports the following platforms:
{{ cookiecutter.platforms | replace('[', '') | replace(']', '') }}

## Prerequisites

- Holoscan SDK {{ cookiecutter.holoscan_version }}
- CUDA (if using GPU acceleration)
- Docker (for containerized deployment)

## Build and Run

Run these commands from the **Holoscan Sensor Bridge Hub repository root**:

```bash
./hsb build {{ cookiecutter.project_slug }} --dryrun --verbose
./hsb build {{ cookiecutter.project_slug }}
./hsb run {{ cookiecutter.project_slug }} --dryrun --verbose
./hsb run {{ cookiecutter.project_slug }}
```

The CLI builds this application's Dockerfile using the repository root as its
Docker context, mounts the checkout, and runs the command from `metadata.json`.
The image includes the CLI version pinned in the root `requirements-cli.txt`;
CMake loads its shared helpers from that installed package.

To open the application's development container:

```bash
./hsb run-container {{ cookiecutter.project_slug }} --dryrun --verbose
./hsb run-container {{ cookiecutter.project_slug }}
```

Inside the container, the same `./hsb build` and `./hsb run` commands execute
locally. For a native SDK installation on the host, add `--local`.

Run the generated smoke test with `./hsb test {{ cookiecutter.project_slug }}`
(preview it first with `--dryrun --verbose`). Extend the test as you add operators.

## Development

### Project Structure

```text
{{ cookiecutter.project_slug }}/
├── CMakeLists.txt
├── Dockerfile
├── README.md
{% if cookiecutter.language == "python" %}├── requirements.txt{% endif %}
├── metadata.json
└── src/
    └── main.{{ 'py' if cookiecutter.language == 'python' else 'cpp' }}
```

### Adding New Operators

1. Create a new operator class in `src/operators/`
2. Include the operator in `src/main.{{ 'py' if cookiecutter.language == 'python' else 'cpp' }}`
3. Update the pipeline configuration

## License

This project is licensed under the {{ cookiecutter.license }} License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Authors

- {{ cookiecutter.full_name }} - {{ cookiecutter.affiliation }}

## Acknowledgments

- NVIDIA Holoscan Team
- Open source community contributors
