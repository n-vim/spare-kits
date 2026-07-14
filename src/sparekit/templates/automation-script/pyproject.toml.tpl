[build-system]
requires = ["hatchling>=1.24"]
build-backend = "hatchling.build"

[project]
name = "{{ project_name }}"
version = "0.1.0"
description = "{{ description }}"
requires-python = ">={{ python_version }}"
authors = [{ name = "{{ author }}" }]
dependencies = ["typer>=0.12.0", "rich>=13.0.0"]

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "ruff>=0.5.0"]

[project.scripts]
{{ package_name }} = "{{ package_name }}.cli:app"

[tool.hatch.build.targets.wheel]
packages = ["src/{{ package_name }}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
