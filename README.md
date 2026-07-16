<div align="center">

# SpareKit

**A Python CLI for creating clean, production-ready starter project kits.**

SpareKit helps you start new Python projects faster by generating well-structured project folders with sensible defaults, useful files, and clean organization.

<br>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)
![Typer](https://img.shields.io/badge/CLI-Typer-0E7C86?style=flat)
![Rich](https://img.shields.io/badge/Terminal-Rich-4B8BBE?style=flat)
![PyYAML](https://img.shields.io/badge/Config-PyYAML-yellow?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Status](https://img.shields.io/badge/Status-Beta-blue?style=flat)

</div>

---

## Overview

SpareKit is a command-line tool built for developers who do not want to repeat the same setup steps every time they start a new project.

Instead of manually creating folders, writing starter files, setting up test structure, adding configuration, and preparing documentation, SpareKit gives you ready-to-use starter kits that are simple, organized, and practical.

It is designed to keep generated projects clean, readable, and easy to extend.

---

## What SpareKit Does

SpareKit can generate starter projects for common Python use cases such as APIs, CLI tools, automation scripts, Python packages, Streamlit apps, Telegram bots, and data science projects.

It focuses on giving every generated project a strong starting point with:

- Clean folder structure
- Useful starter files
- Python project configuration
- Basic documentation
- Test-ready layout
- Optional workflow files
- Optional Docker support
- Configurable project defaults

---

## Features

- Generate new projects from built-in starter kits
- Interactive project creation mode
- Search and inspect available kits
- Create projects using local defaults from `sparekit.yaml`
- Support for remote GitHub-based kit sources
- Clean terminal output with Rich
- Simple CLI experience powered by Typer
- Python package structure using `src/`
- Test setup with Pytest
- Linting support with Ruff
- Type checking support with Mypy
- Easy to extend with more project kits

---

## Available Starter Kits

| Kit | Purpose |
| --- | --- |
| `fastapi-api` | Build a FastAPI backend API project |
| `flask-api` | Start a lightweight Flask API project |
| `cli-tool` | Create a Python CLI application |
| `python-package` | Create a reusable Python package |
| `streamlit-app` | Build a Streamlit dashboard or web app |
| `automation-script` | Start an automation or scripting project |
| `telegram-bot` | Create a Telegram bot project |
| `data-science` | Start a clean data science workspace |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/n-vim/spare-kits.git
cd spare-kits
```

Install SpareKit locally:

```bash
python -m pip install -e .
```

For development setup:

```bash
python -m pip install -e ".[dev]"
```

Check if the CLI is working:

```bash
sparekit --help
```

---

## Usage

Create a FastAPI project:

```bash
sparekit create fastapi-api my-api
```

Create a CLI tool:

```bash
sparekit create cli-tool my-cli
```

Create a Python package:

```bash
sparekit create python-package my-package
```

Create a Streamlit app:

```bash
sparekit create streamlit-app dashboard-app
```

Create an automation project:

```bash
sparekit create automation-script file-cleaner
```

---

## Interactive Mode

Run the create command without arguments to use interactive mode:

```bash
sparekit create
```

SpareKit will guide you through the setup process and ask for the required details such as project name, kit type, author name, and optional features.

This is useful when you want a guided project setup instead of writing the full command manually.

---

## Commands

| Command | Description |
| --- | --- |
| `sparekit list` | Show all available starter kits |
| `sparekit search <query>` | Search kits by name or description |
| `sparekit info <kit>` | Show details about a starter kit |
| `sparekit create <kit> <name>` | Generate a new project |
| `sparekit init` | Create a local `sparekit.yaml` config file |
| `sparekit --help` | Show help information |

---

## Example Workflow

Create a new API project:

```bash
sparekit create fastapi-api task-manager-api
```

Move into the generated project:

```bash
cd task-manager-api
```

Install dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Start building your project.

---

## Configuration

SpareKit supports a local configuration file named `sparekit.yaml`.

Create one with:

```bash
sparekit init
```

Example configuration:

```yaml
author: Nitish Vimal
python_version: "3.11"
include_tests: true
include_github_actions: true
include_docker: false
```

This allows you to reuse your preferred defaults when generating new projects.

---

## Remote Kit Sources

SpareKit can also create projects from kit sources hosted on GitHub.

Example:

```bash
sparekit create my-kit my-project --from github:owner/repository
```

You can also use a specific folder path from a repository:

```bash
sparekit create my-kit my-project --from github:owner/repository/path/to/kits
```

This is useful if you want to maintain your own custom starter kits separately.

---

## Project Structure

The main SpareKit repository is organized like this:

```text
spare-kits/
├── src/
│   └── sparekit/
│       ├── cli.py
│       ├── config.py
│       ├── exceptions.py
│       ├── models.py
│       ├── sources.py
│       ├── templates.py
│       ├── utils.py
│       └── templates/
├── tests/
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

The structure keeps the CLI source code, built-in kits, and tests separated clearly.

---

## Built With

| Tool | Use |
| --- | --- |
| Python | Main programming language |
| Typer | CLI framework |
| Rich | Beautiful terminal output |
| PyYAML | YAML config file support |
| Pytest | Testing |
| Ruff | Linting |
| Mypy | Static type checking |
| Hatchling | Python package build backend |

---

## Development

Install development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run linting:

```bash
ruff check .
```

Run type checking:

```bash
mypy src
```

---

## Why This Project Exists

Most developers create the same basic files again and again when starting a new project. SpareKit reduces that repeated work by giving you a clean starting point instantly.

The goal is not to generate huge or confusing projects. The goal is to create a simple, professional base that developers can understand, run, and improve.

---

## Good Use Cases

SpareKit is useful for:

- Starting new Python projects quickly
- Creating consistent project structures
- Learning how clean Python projects are organized
- Building CLI tools
- Creating small APIs
- Preparing open-source repositories
- Avoiding repeated setup work
- Maintaining reusable project kits

---

## Roadmap

Planned improvements:

- More built-in starter kits
- Kit validation command
- Better remote kit management
- Plugin-style custom kits
- Project preview before generation
- Optional license generation
- Optional pre-commit setup
- More advanced kit metadata
- Better documentation generation

---

## Contributing

Contributions are welcome.

You can help by:

- Adding new starter kits
- Improving existing kits
- Fixing bugs
- Improving documentation
- Adding tests
- Suggesting new features

Before contributing, make sure the project stays simple, clean, and easy to understand.

---

## Author

Created by **Nitish Vimal**.

GitHub: [n-vim](https://github.com/n-vim)

---

## License

This project is licensed under the MIT License.

---

<div align="center">

**SpareKit helps you start faster, stay organized, and build cleaner projects.**

</div>
