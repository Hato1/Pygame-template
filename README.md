# Template for Pygame projects

This template provides:

* A basic pygame project layout with main loop.
* Dependency management with UV.
* Pre-commit configured for:
  * Static type checking with Mypy.
  * Code linting with Ruff.
* A configured github action for automatic web deployment with Pygbag.
* Pyinstaller configured for single file EXE builds on Windows.

TODO: Add py2app for APP builds on MacOS.



## How to use this template

After copying the template, follow these steps:

1. In `pyproject.toml` set desired python version in `requires-python`.
2. [Install UV](https://docs.astral.sh/uv/getting-started/installation/).
3. Navigate to the project directory and run `uv sync`. This will install the correct version of Python (if unavailable) along with all dependencies. A uv lock file will also be created, ensure you commit this so all project checkouts share exact dependency versions.
4. Install pre-commit with `uv run pre-commit install`. Now when you attempt to commit, the scripts in `.pre-commit-config` will run automatically.
