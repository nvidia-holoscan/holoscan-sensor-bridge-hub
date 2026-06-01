# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Overview

This application is built using Holoscan SDK version {{ cookiecutter.holoscan_version }} and supports the following platforms:
{{ cookiecutter.platforms | replace('[', '') | replace(']', '') }}

## Prerequisites

- Holoscan SDK {{ cookiecutter.holoscan_version }}
- CUDA (if using GPU acceleration)
- Docker (for containerized deployment)

## Installation

1. Clone this repository

2. Install dependencies:

3. Build the application:

```bash
cmake -B build -S . -DAPP_{{ cookiecutter.project_slug }}=ON
cmake --build build
```

## Usage

### Running the Application

Follow the run command in `metadata.json` or run the built binary/script directly after building.

### For containerized deployment

The application includes a Dockerfile for containerized deployment:

```bash
# Build the container
docker build -t {{ cookiecutter.project_slug }}:dev .

# Run the containerized application
docker run --gpus all -it --rm \
  -v "$(pwd)":/workspace/{{ cookiecutter.project_slug }} \
  -w /workspace/{{ cookiecutter.project_slug }} \
  {{ cookiecutter.project_slug }}:dev
```

## Development

### Project Structure

```text
{{ cookiecutter.project_slug }}/
├── CMakeLists.txt
├── Dockerfile
├── README.md
{% if cookiecutter.language == "python" %}├── requirements.txt{% endif %}
├── src/
│   └── main.{{ 'py' if cookiecutter.language == 'python' else 'cpp' }}
├── include/
├── tests/
└── docs/
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
