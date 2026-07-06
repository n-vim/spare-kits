[build-system]
requires = ["hatchling>=1.24"]
build-backend = "hatchling.build"

[project]
name = "{{ project_name }}"
version = "0.1.0"
description = "{{ description }}"
requires-python = ">={{ python_version }}"
authors = [{ name = "{{ author }}" }]
dependencies = [
  "fastapi>=0.111.0",
  "uvicorn[standard]>=0.30.0",
  "pydantic-settings>=2.3.0"
]

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "httpx>=0.27.0", "ruff>=0.5.0"]

[tool.hatch.build.targets.wheel]
packages = ["{{ package_name }}"]

[tool.ruff]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
