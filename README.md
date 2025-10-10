# Template for Pygame projects

This template provides:

* A basic pygame project layout with main loop.
* Dependency management with UV.
* Pre-commit configured for:
  * Static type checking with Mypy.
  * Code linting with Ruff.
* A configured github action for automatic web deployment with Pygbag.
* Pyinstaller configured for single file EXE builds on Windows.



## How to use this template

After copying the template, follow these steps:

1. First [set up the development environment](#How-to-setup-development-environment).
2. Install pre-commit with `uv run pre-commit install`. Now when you attempt to commit, the scripts in `.pre-commit-config` will run automatically.


## How to setup development environment

1. Install [dependency manager UV](https://docs.astral.sh/uv/getting-started/installation/).
1. Navigate to project directory.
1. Install pre-commit hooks: `uv run pre-commit install`.
1. Run game: `uv run my-game`.

VSCode should automatcally find the virtual environment created by UV.

Tired of typing `uv run` before every command? Activate the virtual environment with `source .venv/bin/activate` on unix or `.venv\Scripts\activate` on Windows.


## How to build and package

### Web

TODO: Pygbag github action

### Windows EXE

TODO: PyInstaller github action

### MacOS APP

TODO: PyInstaller github action

### Linux

See [setting up dev environment](#How-to-setup-development-environment).  
TODO: PyInstaller github action


## FAQ

### What is UV?

### What is Pre-commit?

### What is Mypy?

### What is Ruff?

### What is Pytest?

Answers for frequently asked questions cost extra.