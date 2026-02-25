# 🎮 Pygame Project Template

A clean, production-ready template for building structured Pygame projects with modern Python tooling.

### ✨ Features:
* 🧠 State machine architecture (Main Menu, Level1, etc.)
* 🎨 Centralised asset loader
  * Works in packaged builds
  * Compatible with Pygbag web builds
* 🎮 Example playable game
* 📦 Dependency management with UV
* 🧹 Pre-commit hooks configured for:
  * Static type checking with Mypy
  * Linting with Ruff
* 🧪 Pytest with example tests
* 🏗️ PyInstaller configuration for:
  * Windows .exe
  * macOS .app
  * Linux binary
* 🚀 Automatic cross-platform builds via GitHub Actions
  * Build for Windows, Mac, and Linux - even if you don't own those systems

## Getting Started
1. [Install UV](https://docs.astral.sh/uv/getting-started/installation/)
2. Navigate to your project
```bash
cd your-project-folder
```
3. (Optional) Install pre-commit hooks.
```bash
uv run pre-commit install
```
4. Run the test game
```bash
uv run run-game
```


>####  💡 Optional: Activate the virtual environment  
> If you're tired of typing `uv run`, this will activate your environment for the session:
> ```bash
> # On macOS and Linux.
> source .venv/bin/activate
> 
> # On Windows.
> .venv\Scripts\activate
> ```
> Now you can run the test game with simply `run-game`.

> 💡 Make sure your IDE is using the virtual environment created by UV.
> * VSCode should detect it automatically.
> * If not, manually select .venv.



## 🏗️ Automatic Builds (Recommended)

After pushing changes to GitHub:

1. Create a Release
2. GitHub Actions will automatically:
    * Build Windows .exe
    * Build macOS .app
    * Build Linux binary
    * Attach them all to the release


## 🔧 Manual Builds

Use this if you need to debug or customize build settings.


### 🌐 Web Build (Pygbag)

> ⚠️ Warning:
> Web builds allow mobile users to play.  
Mobile users often do not have keyboards or mice.  
> Pygbag treats screen taps as left mouse clicks.

TODO: Update this section when Pygbag > 0.9.2 is stable.

---

### 🖥️ Windows EXE / macOS App / Linux Binary

Builds for the current OS and architecture (x86 / ARM).

> 💡 Rule of thumb:
Build on the oldest OS version you want to support.
Applications are usually forward-compatible, not backward-compatible.

Run:
```bash
uv run tools/create_exe.py
```
This will:
1. Populate a `build` directory
2. Output the final executable in `dist` in both "one file" and "many file" formats.


## ❓ FAQ
>### What is UV and why should I use it?
>
>TODO

>### What is Pre-commit?
>A tool that runs checks (linting, formatting, typing) before each commit. After checking out the project it must be installed to run. This project is configured to run Mypy and Ruff checks by default.

>### What is Mypy and why should I use it?
>
>TODO

>###  What is Ruff and why should I use it?
>
>TODO

>### What is Pytest and why should I use it?
>
>TODO

>### What is a state system and why should I use it?
>A state system is a clean way to manage game screens like:
>* Main Menu
>* Settings
>* Level 1
>* Game Over  
>Without it, things can get confusing and it's easy not to properly set up, pack up and reset differents parts of a project. This can lead to bugs and difficult to maintain code.

>### How do GitHub Actions builds work?
>
>TODO
