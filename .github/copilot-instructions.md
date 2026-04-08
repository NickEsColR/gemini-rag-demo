# GitHub Copilot Instructions

## Python Package Management

This project uses **[uv](https://docs.astral.sh/uv/)** as the exclusive Python package and project manager. All suggestions, commands, and workflows involving Python dependencies must follow these conventions:

### Rules

- **Never suggest `pip`, `pip3`, `poetry`, `pipenv`, or `conda`** for installing, removing, or managing packages. Always use `uv` equivalents.
- **Never suggest modifying `requirements.txt` directly.** Dependencies are managed through `pyproject.toml` via `uv`.
- Always use `uv run` to execute Python scripts and tools within the project environment, ensuring the correct virtual environment is used automatically.

### Common `uv` Commands

| Task | Command |
|---|---|
| Install all dependencies | `uv sync` |
| Add a new dependency | `uv add <package>` |
| Add a dev dependency | `uv add --dev <package>` |
| Remove a dependency | `uv remove <package>` |
| Run a script | `uv run python main.py` |
| Run a tool (e.g., pytest) | `uv run pytest` |
| Create/update lockfile | `uv lock` |
| Show installed packages | `uv pip list` |

### Project Structure Conventions

- `pyproject.toml` is the single source of truth for dependencies and project metadata.
- `uv.lock` must be committed to version control to ensure reproducible environments.
- Do not commit `.venv/` to version control (ensure it is listed in `.gitignore`).

### Environment Setup

When onboarding or setting up the project from scratch, the correct command is:

```bash
uv sync
```

This creates the virtual environment and installs all dependencies as defined in `uv.lock`.
