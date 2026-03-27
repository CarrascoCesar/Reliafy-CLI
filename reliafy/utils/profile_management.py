"""
profile_management.py
Utility functions for managing configuration profiles.
Copyright (c) 2025 Cesar Carrasco. All rights reserved.
"""

from collections import OrderedDict
from pathlib import Path

import typer
import yaml
from pydantic_core import ValidationError
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from reliafy.config.data_models import LSFoptions, ReliabilityOptions, ReportingOptions, RFADoptions, RunConfiguration
from reliafy.utils.icons import ICON_ERR
from reliafy.utils.path_helpers import get_profiles_dir

console = Console()


def _dump_top_level_item(key: str, value) -> str:
    """Render one top-level YAML item without sorting keys."""
    return yaml.safe_dump({key: value}, default_flow_style=False, indent=2, line_break="\n", sort_keys=False).strip()


def _dump_yaml_scalar(value) -> str:
    """Render a scalar value using YAML formatting rules."""
    dumped = yaml.safe_dump({"value": value}, default_flow_style=False, sort_keys=False).strip()
    return dumped.split(":", 1)[1].lstrip()


def _format_reliability_options_section(reliability_options: dict) -> str:
    """Render reliability options with grouped comments for readability."""
    lines = ["reliability_options:"]
    emitted_keys = set()

    for group_name, field_names in ReliabilityOptions.PROFILE_GROUPS:
        present_fields = [field_name for field_name in field_names if field_name in reliability_options]
        if not present_fields:
            continue

        lines.append(f"  # {group_name}")
        for field_name in present_fields:
            lines.append(f"  {field_name}: {_dump_yaml_scalar(reliability_options[field_name])}")
            emitted_keys.add(field_name)
        lines.append("")

    remaining_fields = [field_name for field_name in reliability_options if field_name not in emitted_keys]
    if remaining_fields:
        lines.append("  # Other")
        for field_name in remaining_fields:
            lines.append(f"  {field_name}: {_dump_yaml_scalar(reliability_options[field_name])}")
        lines.append("")

    if lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _format_profile_yaml(profile_data: OrderedDict) -> str:
    """Render a custom profile with readable section spacing and comments."""
    blocks = []
    for key, value in profile_data.items():
        if key == "reliability_options":
            blocks.append(_format_reliability_options_section(value))
        else:
            blocks.append(_dump_top_level_item(key, value))
    return "\n\n".join(blocks) + "\n"


def default_profile_models() -> tuple[RunConfiguration, ReliabilityOptions, RFADoptions, LSFoptions, ReportingOptions]:
    """Return the default configuration models."""
    try:
        run_configuration = RunConfiguration()
        reporting_options = ReportingOptions()
        rfad_plot_options = RFADoptions()
        lsf_plot_options = LSFoptions()
        reliability_options = ReliabilityOptions()

        return run_configuration, reporting_options, rfad_plot_options, lsf_plot_options, reliability_options
    except ValidationError as e:
        console.print(f"{ICON_ERR} Error: Invalid default configuration data.")
        console.print(str(e))
        raise typer.Exit(code=1)


def default_profile_dict() -> OrderedDict:
    """Return the default data models as a dictionary."""
    (
        run_configuration,
        reporting_options,
        rfad_plot_options,
        lsf_plot_options,
        reliability_options,
    ) = default_profile_models()
    default_as_dict = OrderedDict(
        {
            "name": "default",
            "description": "Default configuration profile",
            "run_configuration": run_configuration.model_dump(mode="json"),
            "reporting_options": reporting_options.model_dump(mode="json"),
            "rfad_plot_options": rfad_plot_options.model_dump(mode="json"),
            "lsf_plot_options": lsf_plot_options.model_dump(mode="json"),
            "reliability_options": reliability_options.model_dump(mode="json"),
        }
    )
    return default_as_dict


def save_yaml_profile(profile_name: str, profile_description: str = "", overwrite: bool = False) -> None:
    """Save a new configuration profile (yaml file) with default settings."""
    file_path = get_profiles_dir() / f"{profile_name}.yaml"
    if file_path.exists() and not overwrite:
        console.print(f"{ICON_ERR} Error: Profile '{profile_name}' already exists. Use --overwrite to overwrite.")
        raise typer.Exit(code=1)

    default_as_dict = default_profile_dict()
    default_as_dict.pop("run_configuration", None)  # Exclude run_configuration from saved profiles
    default_as_dict["name"] = profile_name
    default_as_dict["description"] = profile_description

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            f.write(_format_profile_yaml(default_as_dict))
    except Exception as e:
        console.print(f"{ICON_ERR} Error saving profile '{profile_name}': {e}")
        raise typer.Exit(code=1)


def save_result_yaml_profile(file_path: Path, profile_data: dict) -> None:
    """
    Save a request configuration profile (yaml file) from provided data dictionary.
    Used to save the profile used to the results directory.
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            f.write(_format_profile_yaml(profile_data))
    except Exception as e:
        console.print(f"{ICON_ERR} Error saving profile '{file_path.name}' to results directory: {e}")
        raise typer.Exit(code=1)


class OrderedLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader, node):
    loader.flatten_mapping(node)
    return OrderedDict(loader.construct_pairs(node))


OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def load_yaml_profile(profile_name: str) -> dict:
    """Load a configuration profile (yaml file) and return as a dictionary."""
    file_path = get_profiles_dir() / f"{profile_name}.yaml"
    if not file_path.exists():
        console.print(f"{ICON_ERR} Error: Profile '{profile_name}' does not exist.")
        raise typer.Exit(code=1)

    try:
        with open(file_path, "r") as f:
            profile_data = yaml.load(f, Loader=OrderedLoader)

    except Exception as e:
        console.print(f"{ICON_ERR} Error loading profile '{profile_name}': {e}")
        raise typer.Exit(code=1)

    return profile_data


def construct_profile_models(profile_name: str, profile_data: dict) -> None:
    """Construct Pydantic models from profile data dictionary and validate them."""
    profile_headers = profile_data.keys()
    try:
        run_configuration = (
            RunConfiguration.model_validate(profile_data["run_configuration"])
            if "run_configuration" in profile_headers
            else RunConfiguration()
        )
        reporting_options = (
            ReportingOptions.model_validate(profile_data["reporting_options"])
            if "reporting_options" in profile_headers
            else ReportingOptions()
        )
        rfad_plot_options = (
            RFADoptions.model_validate(profile_data["rfad_plot_options"])
            if "rfad_plot_options" in profile_headers
            else RFADoptions()
        )
        lsf_plot_options = (
            LSFoptions.model_validate(profile_data["lsf_plot_options"])
            if "lsf_plot_options" in profile_headers
            else LSFoptions()
        )
        reliability_options = (
            ReliabilityOptions.model_validate(profile_data["reliability_options"])
            if "reliability_options" in profile_headers
            else ReliabilityOptions()
        )

    except ValidationError as e:
        console.print(f"{ICON_ERR} Error: Invalid data in profile '{profile_name}'.")
        console.print(str(e))
        raise typer.Exit(code=1)

    return run_configuration, reporting_options, rfad_plot_options, lsf_plot_options, reliability_options


def load_profile_models(
    profile_name: str,
) -> tuple[RunConfiguration, ReportingOptions, RFADoptions, LSFoptions, ReliabilityOptions]:
    """Load a configuration profile and return as a tuple all the configuration options."""
    if profile_name == "default":
        (
            run_configuration,
            reporting_options,
            rfad_plot_options,
            lsf_plot_options,
            reliability_options,
        ) = default_profile_models()
    else:
        profile_data = load_yaml_profile(profile_name)
        (
            run_configuration,
            reporting_options,
            rfad_plot_options,
            lsf_plot_options,
            reliability_options,
        ) = construct_profile_models(profile_name, profile_data)

    return run_configuration, reporting_options, rfad_plot_options, lsf_plot_options, reliability_options


def load_profile_dict(profile_name: str) -> dict:
    """Load a configuration profile and return as a dictionary."""
    if profile_name == "default":
        profile_data = default_profile_dict()
    else:
        profile_data = load_yaml_profile(profile_name)
    return profile_data


def _dict_to_table(title: str, data: dict, defaults: dict | None = None) -> Table:
    """Render a section dict as a table. If defaults are provided, highlight changed values."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    for k, v in data.items():
        val = _format_value(v)
        if defaults is not None and k in defaults and v != defaults.get(k):
            table.add_row(f"[yellow]{k}[/yellow]", f"[yellow]{val}[/yellow]")
        else:
            table.add_row(str(k), val)
    return table


def _format_value(v):
    if isinstance(v, (list, tuple)):
        if len(v) > 6:
            return f"{v[:6]} ... ({len(v)})"
        return str(v)
    if isinstance(v, dict):
        return "{...}"
    return str(v)


def show_profile_rich(profile_name: str, highlight_changes: bool = True):
    """Display a profile with Rich. If highlight_changes=True, differences vs defaults are shown in yellow."""
    if profile_name == "default":
        profile_data = default_profile_dict()
        profile_data.pop("run_configuration", None)  # Remove run_configuration from default display
    else:
        profile_data = load_yaml_profile(profile_name)
        construct_profile_models(profile_name, profile_data)  # Validate data

    # Root keys
    name = profile_data.get("name", profile_name)
    description = profile_data.get("description", "No description")

    # Build defaults dict only when needed (avoid extra work)
    defaults = None
    if highlight_changes and profile_name != "default":
        defaults = default_profile_dict()

    sections = [
        # (
        #     "Run Configuration",
        #     profile_data.get("run_configuration", {}),
        #     defaults.get("run_configuration") if defaults else None,
        # ), # Exclude run_configuration from display
        (
            "Reporting Options",
            profile_data.get("reporting_options", {}),
            defaults.get("reporting_options") if defaults else None,
        ),
        (
            "RFAD Plot Options",
            profile_data.get("rfad_plot_options", {}),
            defaults.get("rfad_plot_options") if defaults else None,
        ),
        (
            "LSF Plot Options",
            profile_data.get("lsf_plot_options", {}),
            defaults.get("lsf_plot_options") if defaults else None,
        ),
        (
            "Reliability Options",
            profile_data.get("reliability_options", {}),
            defaults.get("reliability_options") if defaults else None,
        ),
    ]

    summary_text = (
        f"[bold cyan]Profile:[/bold cyan] {name}\n"
        f"[bold cyan]Description:[/bold cyan] {description}\n"
        + ("[bold cyan]Highlight:[/bold cyan] [yellow]Changed from defaults[/yellow]" if highlight_changes else "")
    )
    summary_panel = Panel(Text.from_markup(summary_text), title="Profile Summary", border_style="cyan")

    tables = [_dict_to_table(title, data, dft) for title, data, dft in sections]
    console.print(summary_panel)
    console.print(Columns(tables, equal=True, expand=True))


# profile_management.py

# profile_management.py

# profile_management.py
