[build-system]
requires = ["hatchling>=1.24"]
build-backend = "hatchling.build"

[project]
name = "{{ project_name }}"
version = "0.1.0"
description = "{{ description }}"
requires-python = ">={{ python_version }}"
authors = [{ name = "{{ author }}" }]
dependencies = ["pandas>=2.0.0", "numpy>=1.26.0", "scikit-learn>=1.4.0"]

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "ruff>=0.5.0", "jupyterlab>=4.0.0"]

[tool.hatch.build.targets.wheel]
packages = ["src/{{ package_name }}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
