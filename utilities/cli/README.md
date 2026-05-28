# HoloHub CLI

> This in-tree CLI implementation is retained only as legacy source context on
> this branch. The top-level `./holohub` entry point now delegates to the
> standalone [`holoscan-cli`](https://github.com/nvidia-holoscan/holoscan-cli)
> package. Use `./holohub --help` or the upstream `holoscan-cli` README for the
> active command surface.

A command-line interface for managing Holoscan-based applications and workflows. Single tool for the full development lifecycle: setup, build, run, test, package, and maintain.

**Design Goals:**

- **Simplicity**: complex workflows transformed into single intuitive commands
- **Developer experience**: fast iteration cycles with granular build control
- **Consistency**: predictable behavior across project types and deployment targets
- **Extensibility**: easy to add commands; portable across repositories via env var customization
- **Reliability**: comprehensive error handling, fuzzy suggestions, and dry-run support

## Quick Start

```bash
./holohub <command> [options] [arguments]
./holohub -h | --help                    # List all commands
./holohub <command> -h | --help          # Options for a specific command
./holohub list                           # List available projects
```

## Documentation

| Document                                | Description                                                                                   |
| --------------------------------------- | --------------------------------------------------------------------------------------------- |
| [CLI Reference](cli_reference.md)       | Complete command reference: all commands, options, modes, environment variables, and examples |
| [CLI Developer Guide](cli_dev_guide.md) | Implementation invariants, workflow tips, extension guide, and source layout                  |
