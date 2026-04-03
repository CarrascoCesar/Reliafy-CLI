"""
api_utils.py
Utility functions for interacting with the Reliafy API endpoint.
Copyright (c) 2025 Cesar Carrasco. All rights reserved.
"""

import importlib
import importlib.util
import json
import os
import pathlib
import pickle
import platform
import shutil
import subprocess
import sys
import time
import traceback
from collections import OrderedDict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Tuple

import filedialpy
import numpy as np
import requests
from matplotlib import pyplot as plt
from rich.console import Console

from reliafy.utils.auth_cli import get_token
from reliafy.utils.icons import ICON_ASK, ICON_DOWN, ICON_ERR, ICON_INFO, ICON_OK, ICON_WARN
from reliafy.utils.path_helpers import copy_examples_to_working_dir, get_problems_dir, get_results_dir
from reliafy.utils.profile_management import save_result_yaml_profile
from reliafy.utils.utilities import safe_write_json

console = Console()


def get_timestamped_results_dir(base_results_path: Path) -> Path:
    """
    Create and return a timestamped subdirectory for storing results.
    Structure: results/YYYY-MM-DD/HH-MM-SS/

    Args:
        base_results_path: Base results directory

    Returns:
        Path to the timestamped subdirectory
    """
    now = datetime.now()
    date_dir = base_results_path / now.strftime("%Y-%m-%d")
    time_dir = date_dir / now.strftime("%H-%M-%S")
    time_dir.mkdir(parents=True, exist_ok=True)
    return time_dir


def cleanup_old_results(base_results_path: Path, days: int = 30) -> None:
    """
    Remove result directories older than the specified number of days.

    Args:
        base_results_path: Base results directory
        days: Remove results older than this many days (default: 30)
    """
    if not base_results_path.exists():
        return

    cutoff_date = datetime.now() - timedelta(days=days)
    removed_count = 0

    # Iterate through date directories (YYYY-MM-DD)
    for date_dir in base_results_path.iterdir():
        if not date_dir.is_dir():
            continue

        try:
            # Parse directory name as date
            dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
            if dir_date < cutoff_date:
                shutil.rmtree(date_dir)
                removed_count += 1
                console.print(f"{ICON_OK} Removed old results: {date_dir.name}")
        except ValueError:
            # Skip directories that don't match the date format
            continue

    if removed_count > 0:
        console.print(f"{ICON_OK} Cleaned up {removed_count} old result director{'y' if removed_count == 1 else 'ies'}")
    else:
        console.print(f"{ICON_INFO} No old results to clean up (keeping last {days} days)")


def setup_paths():
    """
    Set up the paths for running Reliafy application.

    Returns:
        tuple: (url, results_path, problems_path)
    """
    url = os.getenv("AUTH0_AUDIENCE", "https://reliafy.up.railway.app")
    # url = "http://localhost:8080"

    # Create the directory to store the results if it doesn't exist
    results_path = get_results_dir().resolve()
    results_path.mkdir(parents=True, exist_ok=True)

    # Define the path to the problems directory
    problems_path = get_problems_dir().resolve()
    problems_path.mkdir(parents=True, exist_ok=True)

    return url, results_path, problems_path


def serialize_obj(obj: Any) -> Any:
    """
    Recursively serialize an object for JSON compatibility.

    - Converts numpy arrays -> lists
    - numpy scalars -> Python scalars
    - container types are processed recursively
    - dict keys are converted to strings when not already str
    """
    # Fast path for JSON-safe scalars
    if obj is None or isinstance(obj, (bool, int, float, str)):
        return obj

    # Numpy handling
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()

    # Containers
    if isinstance(obj, dict):
        out: Dict[str, Any] = {}
        for k, v in obj.items():
            # JSON requires string keys
            if not isinstance(k, str):
                k = str(serialize_obj(k))
            out[k] = serialize_obj(v)
        return out

    if isinstance(obj, (list, tuple)):
        return [serialize_obj(v) for v in obj]

    # Fallback — attempt to use __dict__ if available, else str()
    if hasattr(obj, "__dict__"):
        try:
            return serialize_obj(vars(obj))
        except Exception:
            pass

    return str(obj)


def get_exception_source(e: BaseException) -> str:
    """
    Return a short single-line description of where an exception occurred.
    """
    tb_exc = traceback.TracebackException.from_exception(e)
    if tb_exc.stack:
        last_frame = tb_exc.stack[-1]
        filename = pathlib.Path(last_frame.filename).name
        lineno = last_frame.lineno
        func = last_frame.name
        line = last_frame.line or ""
        return f'File "{filename}", line {lineno}, in {func}: {line} {type(e).__name__}: {e}'
    return f"{type(e).__name__}: {e}"


def handle_rate_limit_error(response: requests.Response) -> None:
    """
    Handle rate limit errors with a friendly, multi-line output.
    """
    try:
        error_data = response.json()
    except json.JSONDecodeError:
        console.print(f"{ICON_ERR} RATE LIMIT EXCEEDED", style="bold red")
        console.print(f"{ICON_INFO} Unable to parse rate limit response. Please wait and try again.", style="blue")
        return

    endpoint = error_data.get("endpoint", "Unknown endpoint")
    limit_type = error_data.get("limit_type", "unknown")
    limit_exceeded = error_data.get("limit_exceeded", "Unknown limit")
    all_limits = error_data.get("all_limits", "Unknown limits")
    reason = error_data.get("reason", "Rate limiting active")
    suggestion = error_data.get("suggestion", "Please wait 15 seconds before retrying")

    console.print("\n" + "=" * 60, style="red")
    console.print(f"{ICON_ERR} RATE LIMIT EXCEEDED", style="bold red")
    console.print("=" * 60, style="red")
    console.print(f"{ICON_INFO} Endpoint: {endpoint}", style="blue")

    if limit_type == "per_minute":
        console.print(f"{ICON_WARN} Minute Limit Exceeded: {limit_exceeded}", style="yellow")
        console.print(f"{ICON_INFO} All Limits: {all_limits}", style="blue")
        console.print(f"{ICON_INFO} This means you're making requests too quickly", style="blue")
    elif limit_type == "per_day":
        console.print(f"{ICON_WARN} Daily Limit Exceeded: {limit_exceeded}", style="yellow")
        console.print(f"{ICON_INFO} All Limits: {all_limits}", style="blue")
        console.print(f"{ICON_INFO} You've used up your daily quota", style="blue")
    else:
        console.print(f"{ICON_WARN} Limit Exceeded: {limit_exceeded}", style="yellow")
        console.print(f"{ICON_INFO} All Limits: {all_limits}", style="blue")

    console.print(f"{ICON_INFO} Reason: {reason}", style="blue")
    console.print(f"{ICON_INFO} Suggestion: {suggestion}\n", style="blue")


def handle_other_http_errors(response: requests.Response, context_msg: str = "Error") -> None:
    """
    Print an HTTP error message from a Response.
    """
    console.print("\n" + "=" * 60, style="red")
    try:
        error_data = response.json()
        detail = error_data.get("detail", error_data)
        console.print(f"{ICON_ERR} {context_msg}: status code: {response.status_code}: {detail}", style="red")
    except json.JSONDecodeError:
        console.print(f"{ICON_ERR} {context_msg}: status code: {response.status_code}: {response.text}", style="red")
    finally:
        console.print("=" * 60 + "\n", style="red")


def download_single_file(
    url: str,
    file_type: str,
    request_id: str,
    max_retries: int = 3,
    timeout: int = 30,
    headers: Dict[str, str] | None = None,
) -> requests.Response:
    """
    Download a single file with retry and backoff.

    Returns a successful requests.Response or raises last exception.
    """
    file_url = f"{url.rstrip('/')}/{file_type}"
    params = {"request_id": request_id}

    for attempt in range(max_retries + 1):
        try:
            resp = requests.get(file_url, params=params, timeout=timeout, headers=headers)
            resp.raise_for_status()
            return resp

        except requests.exceptions.RequestException as e:
            is_last = attempt == max_retries

            resp_obj = getattr(e, "response", None)
            if resp_obj is not None:
                status = resp_obj.status_code
                # Handle 429 (rate limit) - should retry
                if status == 429:
                    console.print(
                        f"{ICON_INFO} Rate limited downloading {file_type} (attempt {attempt + 1}/{max_retries + 1})",
                        style="blue",
                    )
                    handle_rate_limit_error(resp_obj)
                    if not is_last:
                        wait_time = (2**attempt) + (0.1 * attempt)
                        time.sleep(wait_time)
                        continue
                    else:
                        raise
                # Handle other 4xx client errors - don't retry
                elif 400 <= status < 500:
                    console.print(f"{ICON_ERR} Client error downloading {file_type} (status {status})", style="red")
                    handle_other_http_errors(resp_obj, f"Error downloading {file_type} file")
                    raise
                # 5xx server errors - retry
                elif status >= 500:
                    if not is_last:
                        wait_time = (2**attempt) + (0.1 * attempt)
                        console.print(
                            f"{ICON_WARN} Server error ({status}) downloading {file_type}, retrying in {wait_time:.1f}s..."
                        )
                        time.sleep(wait_time)
                        continue
                    else:
                        handle_other_http_errors(resp_obj, f"Failed to download {file_type} after retries")
                        raise
            else:
                # Network-level errors (no response) - retry
                if not is_last:
                    wait_time = (2**attempt) + (0.1 * attempt)
                    console.print(
                        f"{ICON_WARN} Network error downloading {file_type}: {e}. Retrying in {wait_time:.1f}s..."
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    console.print(f"{ICON_ERR} Failed downloading {file_type} after retries: {e}")
                    raise


def download_results(
    url: str, problem_json: json, results_dir: Path, reporting_options: Dict, max_retries: int = 3
) -> Tuple[List[Path], List[bool]]:
    """
    Download excel/pdf/pickle files for a completed problem.
    Files are saved directly to the provided results_dir (should be timestamped).

    Args:
        url: API base URL
        problem_json: Problem dictionary with Request_ID
        results_dir: Directory to save results (typically timestamped)
        reporting_options: Options for what files to download
        max_retries: Number of retry attempts for failed downloads

    Returns (file_paths, downloaded_flags)
    """
    results_dir = Path(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

    file_types = ["xlsx", "pdf", "pickle"]

    should_download = [
        reporting_options["save_excel_summary"],
        reporting_options["save_plots_to_pdf"] and ("FigureHandles" in problem_json),
        reporting_options["save_plots_to_pickle"] and ("FigureHandles" in problem_json),
    ]

    request_id = problem_json.get("Request_ID", "unknown")
    file_paths: List[Path] = [Path(results_dir, f"{problem_json['name']}-{request_id[-5:]}.{ft}") for ft in file_types]
    request_id = problem_json["Request_ID"]

    downloaded = [False] * len(file_types)

    for idx, (ftype, want, path) in enumerate(zip(file_types, should_download, file_paths)):
        if not want:
            continue

        try:
            console.print(f"{ICON_DOWN} Downloading {ftype} ...")
            # include auth header if available (some deployments may require it)
            headers = None
            # Attempt to get a token if present in reporting_options or environment (non-invasive)
            # (We'll not automatically fetch tokens here to avoid unexpected logins.)
            resp = download_single_file(url, ftype, request_id, max_retries=max_retries, headers=headers)
            with open(path, "wb") as f:
                f.write(resp.content)
            downloaded[idx] = True
            console.print(f"{ICON_OK} Saved {path.name}")
        except requests.exceptions.RequestException:
            console.print(f"{ICON_WARN} Skipping {ftype} (download failed)")
            downloaded[idx] = False

    # console.print()
    # if any(downloaded):
    #     console.print(f"{ICON_OK} Files saved to: {results_dir}")
    # else:
    #     console.print(f"{ICON_WARN} No files were downloaded to: {results_dir}")
    console.print()

    return file_paths, downloaded


def open_file_cross_platform(path: Path) -> None:
    """
    Open a file using the OS default application. Safe for macOS/Windows/Linux.
    """
    try:
        p = str(path)
        system = platform.system()
        if system == "Darwin":
            subprocess.call(["open", p])
        elif system == "Windows":
            # prefer os.startfile if available (simple)
            try:
                os.startfile(p)  # type: ignore[attr-defined]
            except Exception:
                # fallback to subprocess
                subprocess.Popen([p], shell=True)
        else:
            subprocess.call(["xdg-open", p])
    except Exception as e:
        console.print(f"{ICON_ERR} Failed to open {path.name}: {get_exception_source(e)}")


def open_result_files(file_paths: List[Path], file_downloaded: List[bool]) -> None:
    """
    Open downloaded files (skips pickle) using the system viewer.
    """
    for got, path in zip(file_downloaded, file_paths):
        if not got or path.suffix == ".pickle":
            continue
        open_file_cross_platform(path)


def show_pickle_plots(
    problem: Dict, file_paths: List[Path], reporting_options: Dict, file_downloaded: List[bool]
) -> None:
    """
    If pickled matplotlib figures were downloaded, load them, display them non-blocking,
    and wait for the user to hit return before closing.
    """
    if not (
        reporting_options["save_plots_to_pickle"]
        and file_downloaded
        and file_downloaded[2]
        and "FigureHandles" in problem
    ):
        return

    pickle_path = file_paths[2]

    try:
        with open(pickle_path, "rb") as f:
            figs_to_show = pickle.load(f)
    except Exception as e:
        console.print(f"{ICON_ERR} Failed to load pickle file: {e}")
        traceback.print_exc()
        return

    # API always pickles a list of Figure objects
    if not isinstance(figs_to_show, list) or not figs_to_show:
        console.print(f"{ICON_WARN} No valid matplotlib figures found in pickle.")
        return

    # Display all figures
    for fig in figs_to_show:
        if isinstance(fig, plt.Figure):
            plt.figure(fig.number)

    plt.show(block=False)
    try:
        input("⌨️ Hit [return] to end")
    except KeyboardInterrupt:
        pass
    finally:
        plt.close("all")


def load_problem_from_module(problem_file_path: Path) -> Dict | None:
    """
    Load a problem module to check for errors prior to sending to the API.
    Temporarily disables bytecode generation to avoid __pycache__.
    Returns the problem dict or None on failure.
    """
    original_flag = getattr(sys, "dont_write_bytecode", False)
    try:
        # Prevent __pycache__ creation while importing user problem modules
        sys.dont_write_bytecode = True

        module_spec = importlib.util.spec_from_file_location(problem_file_path.stem, problem_file_path)
        if module_spec is None or module_spec.loader is None:
            raise ImportError(f"Could not create module spec for {problem_file_path}")

        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)

        if hasattr(module, "Problem"):
            return module.Problem()
        if hasattr(module, "problem"):
            return module.problem()

        raise AttributeError(f"The problem module '{problem_file_path.name}' does not contain Problem() or problem()")
    except Exception as e:
        src = get_exception_source(e)
        console.print(f"{ICON_ERR} Error loading problem module {problem_file_path.name}: {src}\n")
        return None
    finally:
        sys.dont_write_bytecode = original_flag


def validate_problem_module(problem_file_path: Path, run_configuration: Dict) -> bool:
    """
    Validate that the problem is well defined.
    This is a minimal check to catch errors before sending to the API.
    """
    problem = load_problem_from_module(problem_file_path)
    if problem is None:
        return False

    if run_configuration["run_type"].lower() == "design" and "DesignProblem" not in problem:
        console.print(
            f"{ICON_ERR} Design problem missing 'DesignProblem' key. Did you mean to set run_type = 'analysis'?"
        )
        return False

    return True


def run_app(
    run_configuration: Dict,
    reporting_options: Dict,
    rfad_plot_options: Dict,
    lsf_plot_options: Dict,
    reliability_options: Dict,
    profile_name: str = "",
    open_results: bool = False,
    problem_file_path: Path | None = None,
) -> Dict:
    """
    Post the problem module and options to the API, then download and open results.
    Returns the problem dictionary returned by the server.
    """
    # 0) Setup paths
    url, results_path, problems_path = setup_paths()

    # 1) Get token
    access_token = get_token()
    if not access_token:
        console.print(f"{ICON_ERR} Authentication failed. Please try logging in again.")
        console.print(f"{ICON_INFO} Tip: Run the {run_configuration['run_type']} command once more to trigger login.")
        raise SystemExit(1)

    # 2a) If problems directory is empty, give users option to copy examples
    if not any(problems_path.glob("*.py")):
        console.print(f"{ICON_INFO} Problems directory is empty: {problems_path}")
        if console.input(
            f"{ICON_ASK} Would you like to copy example problem files to this directory? [Y/n]: "
        ).strip().lower() in [
            "",
            "y",
            "yes",
        ]:
            copy_examples_to_working_dir(problems_path)
            console.print(f"{ICON_OK} Example problem files copied to: {problems_path}\n")
        else:
            console.print(f"{ICON_WARN} No problem files available. Please add problem .py files to: {problems_path}\n")
            console.print(f"{ICON_INFO} Exiting.")
            raise SystemExit(1)

    # 2b) Ask user for problem file
    if problem_file_path is None:
        console.print(f"{ICON_INFO} Please select a problem file from the popup menu.\n")
        selected_file = get_problem_file_name(Path(problems_path))
        if not selected_file:
            raise SystemExit(1)
    else:
        selected_file = str(problem_file_path)

    problem_file_path = Path(selected_file)
    valid = validate_problem_module(problem_file_path, run_configuration)
    if not valid:
        console.print(f"{ICON_ERR} Cannot proceed with invalid problem module: {problem_file_path.name}")
        raise SystemExit(1)

    console.print(f"{ICON_OK} Successfully validated problem module: {problem_file_path.name}")

    # 3) Build options (serialized)
    options_payload = {
        "run_configuration": run_configuration,
        "reporting_options": reporting_options,
        "rfad_plot_options": rfad_plot_options,
        "lsf_plot_options": lsf_plot_options,
        "reliability_options": reliability_options,
    }
    options = {"options": json.dumps(serialize_obj(options_payload))}

    # 4) POST to /run_app
    headers = {"Authorization": f"Bearer {access_token}"}
    post_resp = None
    try:
        with console.status(f"[bold green]Processing {problem_file_path.name}..."):
            with open(problem_file_path, "rb") as file_obj:
                files = {"file": file_obj}
                post_resp = requests.post(f"{url.rstrip('/')}/run_app", files=files, data=options, headers=headers)
                post_resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Distinguish between HTTP responses vs. network-level failures
        if post_resp is not None:
            if post_resp.status_code == 429:
                handle_rate_limit_error(post_resp)
            else:
                handle_other_http_errors(post_resp, "App request failed")
        else:
            # Network-level error: connection refused, DNS failure, timeouts, etc.
            # Provide clearer guidance when the API host is unreachable.
            down_msg_printed = False
            try:
                # requests wraps underlying exceptions; check for ConnectionError/Timeout
                if isinstance(e, requests.exceptions.ConnectionError):
                    down_msg_printed = True
                    console.print(
                        f"{ICON_ERR} Unable to reach the API host (connection refused). The service may be temporarily unavailable.",
                        style="red",
                    )
                    console.print(
                        f"{ICON_INFO} Checked URL: {url}. Please try again later or contact support if the issue persists.",
                        style="blue",
                    )
                elif isinstance(e, requests.exceptions.Timeout):
                    down_msg_printed = True
                    console.print(
                        f"{ICON_ERR} API request timed out. The service may be temporarily unavailable or unreachable.",
                        style="red",
                    )
                    console.print(
                        f"{ICON_INFO} Checked URL: {url}. Please try again later or contact support.",
                        style="blue",
                    )
                else:
                    # Inspect the underlying error (e.g., OSError with errno ECONNREFUSED / 61)
                    cause = getattr(e, "__cause__", None) or getattr(e, "__context__", None)
                    if isinstance(cause, OSError) and getattr(cause, "errno", None) in {61, 111}:
                        # 61: macOS ECONNREFUSED, 111: Linux ECONNREFUSED
                        down_msg_printed = True
                        console.print(
                            f"{ICON_ERR} Connection refused when contacting the API. The service appears unavailable.",
                            style="red",
                        )
                        console.print(
                            f"{ICON_INFO} Checked URL: {url}. Please try again later or contact support.",
                            style="blue",
                        )
            except Exception:
                # Fall through to generic message
                pass

            if not down_msg_printed:
                console.print(f"{ICON_ERR} App request failed: {e}\n")
        sys.exit(1)

    # 5) Parse response
    problem_json = post_resp.json()
    request_id = problem_json.get("Request_ID", "unknown")
    console.print(
        f"{ICON_OK} {str(run_configuration['run_type']).capitalize()} run completed for problem: {problem_json.get('name')} with Request ID: {request_id}\n"
    )

    # 6) Print Info messages (if any) # Currently disabled to reduce console clutter
    # info_list = problem_json.get("Info", [])
    # if info_list:
    #     prefix = "\u2022 "
    #     wrapper = textwrap.TextWrapper(initial_indent=prefix, width=130, subsequent_indent=" " * len(prefix))
    #     console.print(f"{ICON_INFO} Messages:")
    #     for m in info_list:
    #         console.print(wrapper.fill(str(m)))
    # else:
    #     console.print(f"{ICON_INFO} Messages: None\n")
    # console.print()

    # 7) Create timestamped directory for this run
    timestamped_dir = get_timestamped_results_dir(results_path)
    rel_path = timestamped_dir.relative_to(results_path.parent)
    file_uri = timestamped_dir.as_uri()
    console.print(
        f"{ICON_OK} Result files, a copy of the problem file, and the profile will be saved to: [link={file_uri}]{rel_path}[/link]\n"
    )

    # 8) Save server returned problem to timestamped directory as JSON
    out_json_path = Path(timestamped_dir, f"{problem_json.get('name', 'result')}-{request_id[-5:]}.json")
    try:
        safe_write_json(problem_json, out_json_path, indent=4)
        console.print(f"{ICON_OK} Saved problem JSON: {out_json_path.name}")
    except Exception as e:
        console.print(f"{ICON_WARN} Failed saving problem JSON to {out_json_path}: {e}")

    # 10) Download files to the timestamped directory
    file_paths, file_downloaded = download_results(url, problem_json, timestamped_dir, reporting_options, max_retries=3)

    # 11) Optional: Clean up old results (keeping last 30 days by default)
    # Uncomment the line below to enable automatic cleanup
    # cleanup_old_results(results_path, days=30)

    # 12) Save a copy of the problem .py file to the results directory for reference
    try:
        problem_py_copy_path = Path(timestamped_dir, f"{problem_json.get('name', 'result')}-{request_id[-5:]}.py")
        shutil.copy2(problem_file_path, problem_py_copy_path)
        console.print(f"{ICON_OK} Copied problem file to results: {problem_py_copy_path.name}")
    except Exception as e:
        console.print(f"{ICON_WARN} Failed copying problem .py file to results directory: {e}")

    # 13) Save profile to results directory
    profile_data = OrderedDict(
        {
            "name": profile_name,
            "description": f"Configuration profile for '{problem_json.get('name', problem_file_path.stem)}' run",
            "run_configuration": run_configuration,
            "reporting_options": reporting_options,
            "rfad_plot_options": rfad_plot_options,
            "lsf_plot_options": lsf_plot_options,
            "reliability_options": reliability_options,
        }
    )
    profile_path = Path(timestamped_dir, f"profile-{request_id[-5:]}.yaml")
    save_result_yaml_profile(profile_path, profile_data)
    console.print(f"{ICON_OK} Saved configuration profile: {profile_path.name}")

    # 14) Open files and show pickles
    if open_results:
        open_result_files(file_paths, file_downloaded)
        show_pickle_plots(problem_json, file_paths, reporting_options, file_downloaded)
    else:
        console.print()
        console.print(
            f"{ICON_INFO} Results are ready in: [link={file_uri}]{rel_path}[/link]. Use --open-results or -o to open them automatically when running the command.\n"
        )

    return problem_json


def get_problem_file_name(problems_path: Path) -> Path | None:
    """
    Prompt the user to select a problem file.
    Returns the Path or None.
    """
    # Preselect the most recently modified .py file
    py_files = [p for p in problems_path.glob("*.py") if p.is_file()]
    latest_py_file = max(py_files, default=None, key=lambda p: p.stat().st_mtime) if py_files else None

    selected_file = filedialpy.openFile(
        initial_dir=str(problems_path),
        filter="*.py",
        title="Select a problem file",
        initial_file=str(latest_py_file) if latest_py_file else "",
    )
    if selected_file is not None and Path(selected_file).is_file():
        return Path(selected_file)
    return None


def get_problem_file_name_tk(problems_path: Path) -> Path | None:
    """
    Prompt the user to select a problem file using tkinter's native file dialog.
    Returns the Path or None.

    Notes:
    - Uses `initialdir` and `initialfile` to preselect the most recently modified .py.
    - Works on macOS/Windows/Linux with a GUI environment.
    - Falls back to None if tkinter is unavailable or the dialog is cancelled.
    """
    try:
        # Lazy imports to avoid requiring Tk in headless contexts
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        return None

    # Determine a reasonable preselection: most recently modified .py file
    py_files = [p for p in problems_path.glob("*.py") if p.is_file()]
    latest_py_file = max(py_files, default=None, key=lambda p: p.stat().st_mtime) if py_files else None

    # Create a temporary root (hidden) for the dialog
    root = tk.Tk()
    try:
        root.withdraw()
        # Some platforms behave better if the window is lifted
        root.update_idletasks()

        selected = filedialog.askopenfilename(
            initialdir=str(problems_path),
            initialfile=latest_py_file.name if latest_py_file else "",
            title="Select a problem file",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")],
        )
    finally:
        # Ensure Tk resources are cleaned up
        try:
            root.destroy()
        except Exception:
            pass

    if selected:
        p = Path(selected)
        if p.is_file():
            return p
    return None


# api_utils.py

# api_utils.py

# api_utils.py

# api_utils.py

# api_utils.py

# api_utils.py

# api_utils.py
