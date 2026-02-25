# Template for Pygame projects

This template provides:

* A state machine pattern implementation for scenes (Main menu, level1, etc).
* A basic example game.
* Dependency management with UV.
* Pre-commit configured for:
  * Static type checking with Mypy.
  * Code linting with Ruff.
* Pyinstaller configured for single file EXE, APP and binary builds on Windows, Mac and Linux.
* Automatic Windows EXE, Mac APP, and Linux Binary builds without needing to have these operating systems yourself.
* A centralised asset loader that works irrespective of packaging method. This includes Pygbag web builds.
* Pytest with a few example tests



## How to use this template

After copying the template, follow these steps:

1. First [set up the development environment](#How-to-setup-development-environment).
1. 

## How to setup development environment

1. Install [dependency manager UV](https://docs.astral.sh/uv/getting-started/installation/).
1. Navigate to project directory.
1. Optionally, install pre-commit hooks: `uv run pre-commit install`.
1. Run test game: `uv run run-game`.

Ensure your IDE is using the correct virtual environment created by UV. VSCode should find this automatcally.

Tired of typing `uv run` before every command? Activate the virtual environment with `source .venv/bin/activate` on unix or `.venv\Scripts\activate` on Windows.

## Automatic builds

After pushing your changes to Github, create a release. This will trigger a github action that will build your project for Mac, Windows and Linux and automatically attach the resulting EXE, APP and Binary to the release.

TODO: Automatic webapp builds with Pygbag

## How to build and package manually

This is useful for debugging and customising build settings.

### Web

Careful! This makes your game available to mobile users who tend not to have keyboards or mice. Pygbag will treat screen taps as left clicks.

TODO: Wait for Pygbag newer than 0.9.2 before writing this section.

### Windows EXE / MacOS App / Linux Binary

Program will build for the client OS, environment and architecture (i.e x86 or ARM). As a rule of thumb, export on the oldest os you want to be able to run the program as applications are often forwards compatible, but not backwards compatible.

`uv run tools/create_exe.py`

This will populate a build directory before producing the build in a dist directory.


## FAQ

### What is UV?

### What is Pre-commit?

### What is Mypy?

### What is Ruff?

### What is Pytest?

### What is a state system?

### How do the github actions / automatic builds work?

Answers for frequently asked questions cost extra.
