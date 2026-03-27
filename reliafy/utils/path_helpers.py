"""
Minimal helpers that keep user data in the current working directory.
Copyright (c) 2025 Cesar Carrasco. All rights reserved.

Goals:
- Users work in whatever directory they choose in the terminal.
- `problems`, `profiles`, and `results` live in that working directory.
"""

import importlib.resources as resources
import shutil
from pathlib import Path
from typing import List


def get_working_dir() -> Path:
    """Return the current working directory as a Path."""
    return Path.cwd()


def get_problems_dir() -> Path:
    return get_working_dir() / "problems"


def get_profiles_dir() -> Path:
    return get_working_dir() / "profiles"


def get_results_dir() -> Path:
    return get_working_dir() / "results"


def ensure_runtime_dirs() -> None:
    """Create `problems`, `profiles`, and `results` under the current working dir."""
    for path in [get_problems_dir(), get_profiles_dir(), get_results_dir()]:
        path.mkdir(parents=True, exist_ok=True)


def get_packaged_example_problems_dir() -> Path:
    """Locate packaged example problems inside the installed package.

    Works both from source and when installed as a wheel.
    """
    try:
        return Path(resources.files("reliafy")).joinpath("examples", "problems")
    except Exception:
        # Fallback for development if resources resolution fails
        pkg_root = Path(__file__).resolve().parent.parent
        return pkg_root / "examples" / "problems"


def list_packaged_example_problems() -> List[str]:
    """List example problem module base names (without .py)."""
    d = get_packaged_example_problems_dir()
    if not d.exists():
        return []
    return [p.stem for p in d.iterdir() if p.is_file() and p.suffix == ".py"]


def copy_examples_to_working_dir(overwrite: bool = False) -> Path:
    """Copy packaged example problems into the user's working directory `problems/`.

    - Creates `problems/` if missing.
    - If `overwrite` is False, existing files are left untouched.
    Returns the destination problems directory.
    """
    src = get_packaged_example_problems_dir()
    dst = get_problems_dir()
    try:
        dst.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            return dst
        for item in src.iterdir():
            if item.is_file() and item.suffix == ".py":
                target = dst / item.name
                if overwrite or not target.exists():
                    shutil.copy2(item, target)
        return dst
    except Exception as e:
        raise RuntimeError(f"Failed to copy example problems: {e}") from e


# Backward-compatible aliases for existing code that may still import old names
def get_problems_path(override: str | Path | None = None) -> Path:
    return Path(override).expanduser().resolve() if override else get_problems_dir()

# path_helpers.py
