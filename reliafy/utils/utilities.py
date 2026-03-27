import json
import os
import platform
import shutil
import subprocess
from pathlib import Path

from rich.console import Console

from reliafy.utils.icons import ICON_ERR

console = Console()


def safe_write_json(data: json.JSONEncoder, path: Path, indent: int = 4) -> None:
    """
    Atomically write JSON to a file (write tmp then replace).
    Prevent data corruption by ensuring that the original json file
    is only replaced if the new data is fully written.
    """
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
            f.flush()
            os.fsync(f.fileno())
        tmp.replace(path)
        # Ensure directory entry is flushed to disk
        dir_fd = os.open(path.parent, os.O_DIRECTORY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except Exception as e:
        console.print(f"{ICON_ERR} Failed to write JSON file {path}: {e}")


def is_gnu_nano():
    """
    Check if the installed nano editor is GNU nano.
    Returns a tuple (is_gnu: bool, nano_path: str | None)
    """
    nano_path = shutil.which("nano")
    if not nano_path:
        return False, None

    system = platform.system()

    # Windows: version flag works
    if system == "Windows":
        try:
            result = subprocess.run(["nano", "--version"], capture_output=True, text=True, timeout=2)
            if "GNU nano" in result.stdout:
                return True, nano_path
        except Exception:
            pass
        return False, nano_path

    # macOS/Linux: prefer 'strings' when available; otherwise fall back to direct binary scan
    strings_path = shutil.which("strings")
    if strings_path:
        try:
            result = subprocess.run([strings_path, nano_path], capture_output=True, text=True, timeout=2)
            if "GNU nano" in result.stdout:
                return True, nano_path
        except Exception:
            pass
    else:
        # Fallback: read a chunk of the binary and look for the token
        try:
            with open(nano_path, "rb") as f:
                data = f.read(1024 * 1024)  # read first 1MB
                if b"GNU nano" in data:
                    return True, nano_path
        except Exception:
            pass

    return False, nano_path
