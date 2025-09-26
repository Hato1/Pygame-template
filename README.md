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



# FAQ



### What is UV and why do I want it?

UV is a dependency manager like Pip and Poetry that additionally manages Python installations. Dependency managers are important to track and streamline installation of a project's exact requirements. This way, you and any other contributors (or you on other devices) can be sure they have the exact same version of Python, Pygame, and anything else. There's no telling when a new version of a dependency will break something in a weird way.



### What does pre-commit do?

After installing, attempting to commit code will cause the scripts in `.pre-commit-config.yaml` to run. This template is configured to run Mypy and Ruff checks, which if failed will block your commit.

* **Mypy** will check for type errors, similar to Pylance in VSCode.

  It doesn't do much if you don't typehint your code, so don't forget!

  ```py
  def number_halver(number: int) -> int:
      return number / 2
  
  number_halver("Hello World")
  ```

  Mypy finds two errors in this script:

  ```bash
  game.py:2: error: Incompatible return value type (got "float", expected "int")  [return-value]
  game.py:4: error: Argument 1 to "number_halver" has incompatible type "str"; expected "int"  [arg-type]
  Found 2 errors in 1 file (checked 1 source file)
  ```

  Mypy tells us the first error is in game.py line 2. It's complaining that `number_halver` is typehinted to return `int`, but on line 2 we actually return `float`.

  The second error is on line 4

* **Ruff**

These tools will check your code for bugs and style. If the checks fail, your commit will fail. Ruff will attempt to fix some issues automatically, so if there are some new changes, stage them and try again. Otherwise, read the error message and fix up your code.

For users new to these tools, pre-commit can be overwhelming by rejecting your code 'that works'. Instead of turning it off entirely, try removing some/all of Ruff's rules in pyproject.toml in `extend-select`.
