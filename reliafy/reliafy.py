"""
Reliafy CLI - Reliability Analysis and Design Entry Point

A command-line interface for running reliability analysis
and design routines using the Reliafy API.

Copyright (c) 2025 Cesar Carrasco. All rights reserved.

Usage:
    python -m reliafy [OPTIONS] COMMAND [ARGS]...
    python -m reliafy --help
"""

from dotenv import load_dotenv

load_dotenv()
import subprocess
import sys
from pathlib import Path
from pprint import pprint

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from reliafy.config.data_models import IsMethodEnum, RunTypeEnum
from reliafy.utils.api_utils import run_app
from reliafy.utils.auth_cli import get_token, get_user_id
from reliafy.utils.icons import ICON_ASK, ICON_ERR, ICON_INFO, ICON_OK, ICON_RUN, ICON_WARN
from reliafy.utils.path_helpers import (
    copy_examples_to_working_dir,
    ensure_runtime_dirs,
    get_profiles_dir,
    list_packaged_example_problems,
)
from reliafy.utils.profile_management import (
    load_profile_dict,
    load_profile_models,
    load_yaml_profile,
    save_yaml_profile,
    show_profile_rich,
)
from reliafy.utils.utilities import is_gnu_nano

console = Console()
# fmt: off
app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=True, rich_markup_mode="rich")

examples = typer.Typer(help="[green bold]Manage[/green bold] packaged example problems", rich_help_panel="Examples")
app.add_typer(examples, name="examples")

profiles = typer.Typer(help="[green bold]Manage[/green bold] configuration profiles", rich_help_panel="Profile Management")
app.add_typer(profiles, name="profile")

user = typer.Typer(help="[green bold]Manage[/green bold] user authentication", rich_help_panel="User Authentication")
app.add_typer(user, name="user")


@app.callback(help=None)
def _init_runtime_dirs():
    """Initialize working-directory folders on any command invocation."""
    ensure_runtime_dirs()


profile_help = "Profile name for predefined configurations"
use_sorm_help = "Use second order reliability method (SORM) in design optimization"
include_sorm_help = "Include second order reliability (SORM) analysis"
include_mc_help = "Include Monte Carlo (MC) simulation"
include_form_help = "Include first order reliability method (FORM) analysis"
mc_with_is_help = "Use importance sampling (IS) with Monte Carlo (MC) simulation"
plot_rfad_help = "Plot reliability based failure assessment diagram (RFAD)"
plot_lsf_help = "Plot limit state function (LSF)"
plot_pdfs_help = "Plot probability density functions (PDFs) of stochastic variables"
open_results_help = "Open results (e.g., excel report, pdf report and plots)"

@app.command(help="[bold green]Run[/bold green] reliability analysis with specified options")
def analyze(
    profile: Annotated[str, typer.Argument(help=profile_help)] = "default",
    include_sorm: Annotated[
        bool,
        typer.Option("--include-sorm", "-s", help=include_sorm_help, rich_help_panel="Reliability Methods"),
    ] = False,
    include_mc: Annotated[
        bool,
        typer.Option("--include-mc", "-m", help=include_mc_help, rich_help_panel="Monte Carlo"),
    ] = False,
    mc_with_is: Annotated[
        bool,
        typer.Option("--mc-with-is", "-i", help=mc_with_is_help, rich_help_panel="Monte Carlo"),
    ] = False,
    plot_rfad: Annotated[
        bool,
        typer.Option("--plot-rfad","-r", help=plot_rfad_help, rich_help_panel="Plots"),
    ] = False,
    plot_lsf: Annotated[
        bool,
        typer.Option("--plot-lsf", "-l", help=plot_lsf_help, rich_help_panel="Plots")
    ] = False,
    plot_pdfs: Annotated[
        bool,
        typer.Option("--plot-pdfs", "-p", help=plot_pdfs_help,rich_help_panel="Plots"),
    ] = False,
    open_results: Annotated[
        bool,
        typer.Option("--open-results", "-o"), # , help=open_results_help, rich_help_panel="General"),
    ] = True,
):
    """Run reliability analysis with specified options."""
    (
        run_configuration,
        reporting_options,
        rfad_plot_options,
        lsf_plot_options,
        reliability_options,
    ) = load_profile_models(profile) # Load models from profile to validate them

    if profile == "default":
        console.print(f"{ICON_INFO} Using default profile. Specify a profile name to use a custom profile.", style="dim")

    if mc_with_is and not include_mc:
        console.print("Warning: 'mc_with_is' is set to True but 'include_mc' is False. Enabling 'include_mc'.")
        include_mc = True

    # Set fields using validated assignment and Enum members
    run_configuration.run_type = RunTypeEnum.analyze
    run_configuration.include_sorm = include_sorm
    run_configuration.include_mc = include_mc
    run_configuration.mc_with_is = mc_with_is
    run_configuration.plot_rfad = plot_rfad
    run_configuration.plot_lsf = plot_lsf
    run_configuration.plot_pdfs = plot_pdfs

    # Rich table summary of selected options (print title separately to avoid wrapping)
    title = f"{ICON_RUN} Running reliability analysis with '{profile}' profile"
    console.print(f"[bold]{title}[/bold]")
    summary_table = Table(show_lines=False, pad_edge=True)
    summary_table.add_column("include_sorm", style="blue", no_wrap=True)
    summary_table.add_column("include_mc", style="cyan", no_wrap=True)
    summary_table.add_column("mc_with_is", style="cyan", no_wrap=True)
    summary_table.add_column("plot_rfad", style="magenta", no_wrap=True)
    summary_table.add_column("plot_lsf", style="magenta", no_wrap=True)
    summary_table.add_column("plot_pdfs", style="magenta", no_wrap=True)
    # summary_table.add_column("open_results", style="green", no_wrap=True)

    def _fmt(v: bool) -> str:
        return f"[green]True[/green]" if v else "[dim]False[/dim]"

    summary_table.add_row(
        _fmt(include_sorm),
        _fmt(include_mc),
        _fmt(mc_with_is),
        _fmt(plot_rfad),
        _fmt(plot_lsf),
        _fmt(plot_pdfs),
        # _fmt(open_results),
    )
    console.print(summary_table)
    run_app(
        run_configuration.model_dump(mode="json"),
        reporting_options.model_dump(mode="json"),
        rfad_plot_options.model_dump(mode="json"),
        lsf_plot_options.model_dump(mode="json"),
        reliability_options.model_dump(mode="json"),
        profile,
        open_results=open_results,
    )
    console.print()

# Register aliases 'analyse, an' that point to the same function
app.command(name="analyse", help="Alias for analyze", hidden=True)(analyze)
app.command(name="an", help="Alias for analyze", hidden=True)(analyze)

@app.command(help="[bold green]Run[/bold green] reliability-based design optimization with specified options")
def design(
    profile: Annotated[str, typer.Argument(help=profile_help)] = "default",
    use_sorm: Annotated[
        bool,
        typer.Option("--use-sorm", "-s", help=use_sorm_help, rich_help_panel="Reliability Methods")
    ] = False,
    open_results: Annotated[
        bool,
        typer.Option("--open-results", "-o"), # , help=open_results_help, rich_help_panel="General"),
    ] = True,
):
    """Run reliability-based design optimization with specified options."""
    (
        run_configuration,
        reporting_options,
        rfad_plot_options,
        lsf_plot_options,
        reliability_options,
    ) = load_profile_models(profile) # Load models from profile to validate them

    if profile == "default":
        console.print(f"{ICON_INFO} Using default profile. Specify a profile name to use a custom profile.", style="dim")

    run_configuration.run_type = RunTypeEnum.design
    run_configuration.include_sorm = use_sorm
    # Rich table summary (single option for now, extensible later)
    design_title = f"{ICON_RUN} Running design optimization with '{profile}' profile"
    console.print(f"[bold]{design_title}[/bold]")
    design_table = Table(show_lines=False, pad_edge=True)
    design_table.add_column("use_sorm", style="blue", no_wrap=True)
    # design_table.add_column("open_results", style="green", no_wrap=True)
    design_table.add_row(
        "[green]True[/green]" if use_sorm else "[dim]False[/dim]",
        # "[green]True[/green]" if open_results else "[dim]False[/dim]",
    )
    console.print(design_table)
    run_app(
        run_configuration.model_dump(mode="json"),
        reporting_options.model_dump(mode="json"),
        rfad_plot_options.model_dump(mode="json"),
        lsf_plot_options.model_dump(mode="json"),
        reliability_options.model_dump(mode="json"),
        profile,
        open_results=open_results,
    )
    console.print()

# Register aliase 'des' that points to the same function
app.command(name="des", help="Alias for design", hidden=True)(design)


@app.command(help="[bold green]Simulate[/bold green] using Monte Carlo with specified options")
def simulate(
    profile: Annotated[str, typer.Argument(help=profile_help)] = "default",
    mc_with_is: Annotated[
        bool,
        typer.Option("--mc-with-is", "-i", help=mc_with_is_help, rich_help_panel="Monte Carlo"),
    ] = False,
    include_form: Annotated[
        bool,
        typer.Option("--include-form", "-f", help=include_form_help, rich_help_panel="Reliability Methods"),
    ] = False,
    include_sorm: Annotated[
        bool,
        typer.Option("--include-sorm", "-s", help=include_sorm_help, rich_help_panel="Reliability Methods"),
    ] = False,
    plot_lsf: Annotated[
        bool,
        typer.Option("--plot-lsf", "-l", help=plot_lsf_help, rich_help_panel="Plots")
    ] = False,    
    plot_pdfs: Annotated[
        bool,
        typer.Option("--plot-pdfs", "-p", help=plot_pdfs_help, rich_help_panel="Plots"),
    ] = False,
    open_results: Annotated[
        bool,
        typer.Option("--open-results", "-o"), # , help=open_results_help, rich_help_panel="General"),
    ] = True,
):
    """Run Monte Carlo simulation with specified options."""
    (
        run_configuration,
        reporting_options,
        rfad_plot_options,
        lsf_plot_options,
        reliability_options,
    ) = load_profile_models(
        profile
    )  # Load models from profile to validate them

    if profile == "default":
        console.print(f"{ICON_INFO} Using default profile. Specify a profile name to use a custom profile.", style="dim")    
           

    if include_sorm and not include_form:
        console.print(
            "Warning: 'include_sorm' is set to True but 'include_form' is False. Enabling 'include_form'."
        )
        include_form = True

    if reliability_options.is_method == IsMethodEnum.mpp_normal and not include_form:
        console.print(
            "Warning: 'is_method' is set to 'mpp_normal' which requires FORM analysis. Enabling 'include_form'."
        )
        include_form = True

    if (plot_lsf and lsf_plot_options.plot_failure_point) and not include_form:
        console.print(
            "Warning: 'plot_lsf' is set to True to plot failure point(s). Enabling 'include_form'."
        )
        include_form = True

    run_configuration.run_type = RunTypeEnum.simulate
    run_configuration.include_mc = True
    run_configuration.mc_with_is = mc_with_is
    run_configuration.include_form = include_form
    run_configuration.include_sorm = include_sorm
    run_configuration.plot_lsf = plot_lsf
    run_configuration.plot_pdfs = plot_pdfs
    # Rich table summary (no options for now, extensible later)
    sim_title = f"{ICON_RUN} Running Monte Carlo simulation with '{profile}' profile"
    console.print(f"[bold]{sim_title}[/bold]")
    sim_table = Table(show_lines=False, pad_edge=True)
    sim_table.add_column("mc_with_is", style="cyan", no_wrap=True)
    sim_table.add_column("include_form", style="cyan", no_wrap=True)
    sim_table.add_column("include_sorm", style="cyan", no_wrap=True)
    sim_table.add_column("plot_lsf", style="magenta", no_wrap=True)
    sim_table.add_column("plot_pdfs", style="magenta", no_wrap=True)
    # sim_table.add_column("open_results", style="green", no_wrap=True)

    def _fmt(v: bool) -> str:
        return f"[green]True[/green]" if v else "[dim]False[/dim]"

    sim_table.add_row(
        _fmt(mc_with_is),
        _fmt(include_form),
        _fmt(include_sorm),
        _fmt(plot_lsf),
        _fmt(plot_pdfs),
        # _fmt(open_results),
    )

    console.print(sim_table)
    run_app(
        run_configuration.model_dump(mode="json"),
        reporting_options.model_dump(mode="json"),
        rfad_plot_options.model_dump(mode="json"),
        lsf_plot_options.model_dump(mode="json"),
        reliability_options.model_dump(mode="json"),
        profile,
        open_results=open_results,
    )
    console.print()

# Register an alias 'sim' that points to the same function
app.command(name="sim", help="Alias for simulate", hidden=True)(simulate)
# fmt: on


@examples.command(help="[bold green]Copy[/bold green] packaged example problems to working directory")
def copy(
    force: Annotated[
        bool, typer.Option("--force", "-f", help="Overwrite existing files in problems/", rich_help_panel="Examples")
    ] = False,
):
    """Copy packaged example problems into the current working directory's `problems/` folder."""
    try:
        dst = copy_examples_to_working_dir(overwrite=force)
        console.print(f"{ICON_OK} Examples copied to '{dst}'. Overwrite={'yes' if force else 'no'}")
        console.print()
    except Exception as e:
        console.print(f"{ICON_ERR} Error copying examples: {e}")
        console.print()


# Register alias 'cp' that points to the same function
examples.command(name="cp", help="Alias for copy", hidden=True)(copy)


@examples.command(help="[bold green]List[/bold green] packaged example problems")
def list():
    """List packaged example problems available in the installed package."""
    try:
        examples = list_packaged_example_problems()
        if not examples:
            console.print("No packaged example problems found.")
            console.print()
            return
        table = Table(title="Packaged Example Problems:")
        table.add_column("Module Name", style="cyan", no_wrap=True)
        for example in examples:
            table.add_row(example)
        console.print(table)
        console.print()
    except Exception as e:
        console.print(f"{ICON_ERR} Error listing example problems: {e}")
        console.print()


# Register alias 'ls' that points to the same function
examples.command(name="ls", help="Alias for list", hidden=True)(list)


@profiles.command(help="[bold green]Create[/bold green] a new configuration profile with default settings")
def new(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="Name of the profile to create")],
    description: Annotated[
        str, typer.Option("--description", "-d", help="Description of the profile")
    ] = "User-defined profile",
    force: Annotated[bool, typer.Option("--force", "-f", help="Overwrite existing profile if it exists")] = False,
):
    """Create a new configuration profile with default settings to be edited by the user."""
    if name.strip() == "default":
        console.print(f"{ICON_ERR} Error: Cannot create a profile named 'default' as it is reserved.")
        console.print()
        raise typer.Exit(code=1)
    try:
        save_yaml_profile(name, description, force)
        console.print(f"{ICON_OK} Profile '{name}' created with default settings.")
        console.print()
    except Exception as e:
        # Handled in save_yaml_profile
        raise typer.Exit(code=1)
    finally:
        # List profiles after creation
        ctx.invoke(list)


@profiles.command(help="[bold green]Display[/bold green] a configuration profile")
def show(
    name: Annotated[str, typer.Argument(help="Name of the profile to display")],
    raw: Annotated[bool, typer.Option("--raw", "-r", help="Show raw YAML instead of formatted view")] = False,
):
    """Display a configuration profile."""
    if raw:
        profile_data = load_profile_dict(name)
        pprint(profile_data, indent=2)
    else:
        show_profile_rich(name)
    console.print()


# Register alias 'echo' that points to the same function
profiles.command(name="echo", help="Alias for show", hidden=True)(show)


@profiles.command(help="[bold green]List[/bold green] all available configuration profiles")
def list():
    """List all available configuration profiles."""
    try:
        profiles = [p.stem for p in get_profiles_dir().glob("*.yaml")]
        if not profiles:
            console.print("No profiles found in the profiles directory.")
            return
        table = Table(title="Available Configuration Profiles:")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Status", style="magenta")
        table.add_row("Default", "Default profile", f"{ICON_OK} Built-in")
        for profile in profiles:
            profile_data = load_yaml_profile(profile)
            description = profile_data.get("description", "No description")
            status = f"{ICON_INFO} Custom"
            table.add_row(profile, description, status)
        console.print(table)
        console.print()
    except Exception as e:
        console.print(f"{ICON_ERR} Error listing profiles: {e}")
        console.print()


# Register alias 'ls' that points to the same function
profiles.command(name="ls", help="Alias for list", hidden=True)(list)


@profiles.command(help="[bold green]Validate[/bold green] a configuration profile")
def validate(name: Annotated[str, typer.Argument(help="Name of the profile to validate")]):
    """Validate a configuration profile."""
    load_profile_models(name)
    console.print(f"{ICON_OK} Profile '{name}' is valid.")
    console.print()


# Register alias 'val' that points to the same function
profiles.command(name="val", help="Alias for validate", hidden=True)(validate)


@profiles.command(help="[bold yellow]Edit[/bold yellow] a configuration profile with nano")
def nano(
    name: Annotated[str, typer.Argument(help="Name of the profile to edit")],
):
    """Edit a configuration profile using nano in the current terminal."""
    profile_path = get_profiles_dir() / f"{name}.yaml"
    if not profile_path.exists():
        console.print(f"{ICON_ERR} Error: Profile '{name}' does not exist.")
        console.print()
        raise typer.Exit(code=1)

    try:
        is_gnu = is_gnu_nano()[0]
        if not is_gnu:
            subprocess.run(["nano", str(profile_path)], check=False)
        else:
            nanorc = Path(".nanorc")
            cmd = ["nano"]
            if nanorc.exists():
                cmd.append(f"--rcfile={nanorc.as_posix()}")
                # Force YAML syntax highlighting
                cmd.append("--syntax=yaml")
            cmd.append(str(profile_path))
            subprocess.run(cmd, check=False)
        console.print(f"{ICON_OK} Finished editing profile '{name}'.")
        console.print()
    except Exception as e:
        console.print(f"{ICON_ERR} Error: Failed to open profile '{name}' in editor: {e}")
        console.print()
        raise typer.Exit(code=1)


@profiles.command(help="[bold yellow]Edit[/bold yellow] a configuration profile with vim")
def vim(
    name: Annotated[str, typer.Argument(help="Name of the profile to edit")],
):
    """Edit a configuration profile using vim in the current terminal."""
    import subprocess
    from pathlib import Path

    profile_path = get_profiles_dir() / f"{name}.yaml"
    if not profile_path.exists():
        console.print(f"{ICON_ERR} Error: Profile '{name}' does not exist.")
        console.print()
        raise typer.Exit(code=1)

    try:
        vimrc = Path(".vimrc")
        cmd = ["vim"]
        if vimrc.exists():
            cmd += ["-u", vimrc.as_posix()]
        cmd += [str(profile_path)]
        subprocess.run(cmd, check=False)
        console.print(f"{ICON_OK} Finished editing profile '{name}'.")
        console.print()
    except Exception as e:
        console.print(f"{ICON_ERR} Error: Failed to open profile '{name}' in editor: {e}")
        console.print()
        raise typer.Exit(code=1)


# Resister alias 'vi' that points to the same function
profiles.command(name="vi", help="Alias for vim", hidden=True)(vim)


@profiles.command(help="[bold green]Copy[/bold green] an existing configuration profile")
def copy(
    ctx: typer.Context,
    source_name: Annotated[str, typer.Argument(help="Name of the source profile to copy")],
    dest_name: Annotated[str, typer.Argument(help="Name of the new copied profile")],
    validate_before: Annotated[
        bool,
        typer.Option("--validate", "-v", help="Validate source profile before copying"),
    ] = False,
):
    """Copy an existing configuration profile."""
    if source_name.strip() == dest_name.strip():
        console.print(f"{ICON_WARN} Warning: Source name and destination name are the same. No action taken.")
        console.print()
        raise typer.Exit(code=0)

    if dest_name.strip() == "default":
        console.print(f"{ICON_ERR} Error: Cannot copy a profile to 'default' as it is reserved.")
        console.print()
        raise typer.Exit(code=1)

    if source_name.strip() == "default":
        # Use new to create a copy of default
        ctx.invoke(new, ctx=ctx, name=dest_name)
        return

    source_file_path = get_profiles_dir() / f"{source_name}.yaml"
    dest_file_path = get_profiles_dir() / f"{dest_name}.yaml"

    if not source_file_path.exists():
        console.print(f"{ICON_ERR} Error: Profile '{source_name}' does not exist.")
        console.print()
        raise typer.Exit(code=1)
    if dest_file_path.exists():
        console.print(f"{ICON_ERR} Error: Profile '{dest_name}' already exists.")
        console.print()
        raise typer.Exit(code=1)

    if validate_before:
        ctx.invoke(validate, name=source_name)

    try:
        dest_file_path.write_text(source_file_path.read_text())
        console.print(f"{ICON_OK} Profile '{source_name}' has been copied to '{dest_name}'.")
        console.print()
    except Exception as e:
        console.print(f"{ICON_ERR} {e}")
        raise typer.Exit(code=1)
    finally:
        # List profiles after copying
        ctx.invoke(list)


# Register alias 'cp' that points to the same function
profiles.command(name="cp", help="Alias for copy", hidden=True)(copy)


@profiles.command(help="[bold yellow]Rename[/bold yellow] a configuration profile")
def rename(
    ctx: typer.Context,
    old_name: Annotated[str, typer.Argument(help="Current name of the profile")],
    new_name: Annotated[str, typer.Argument(help="New name for the profile")],
    validate_before: Annotated[
        bool,
        typer.Option("--validate", "-v", help="Validate profile before renaming"),
    ] = False,
):
    """Rename a configuration profile."""
    if old_name.strip() == new_name.strip():
        console.print(f"{ICON_WARN} Warning: Old name and new name are the same. No action taken.")
        console.print()
        raise typer.Exit(code=0)

    if new_name.strip() == "default":
        console.print(f"{ICON_ERR} Error: Cannot rename a profile to 'default' as it is reserved.")
        console.print()
        raise typer.Exit(code=1)

    if old_name.strip() == "default":
        console.print(f"{ICON_ERR} Error: Cannot rename the 'default' profile as it is reserved.")
        console.print()
        raise typer.Exit(code=1)

    old_file_path = get_profiles_dir() / f"{old_name}.yaml"
    new_file_path = get_profiles_dir() / f"{new_name}.yaml"

    if not old_file_path.exists():
        console.print(f"{ICON_ERR} Error: Profile '{old_name}' does not exist.")
        console.print()
        raise typer.Exit(code=1)
    if new_file_path.exists():
        console.print(f"{ICON_ERR} Error: Profile '{new_name}' already exists.")
        console.print()
        raise typer.Exit(code=1)

    if validate_before:
        ctx.invoke(validate, name=old_name)

    try:
        old_file_path.rename(new_file_path)
        console.print(f"{ICON_OK} Profile '{old_name}' has been renamed to '{new_name}'.")
        console.print()
    except Exception as e:
        console.print(f"{ICON_ERR} {e}")
        raise typer.Exit(code=1)
    finally:
        # List profiles after renaming
        ctx.invoke(list)


# Register alias 'mv' that points to the same function
profiles.command(name="mv", help="Alias for rename", hidden=True)(rename)


@profiles.command(help="[bold red]Delete[/bold red] a configuration profile")
def delete(ctx: typer.Context, name: Annotated[str, typer.Argument(help="Name of the profile to delete")]):
    """Delete a configuration profile."""
    if name.strip() == "default":
        console.print(f"{ICON_ERR} Error: Cannot delete the 'default' profile as it is reserved.")
        console.print()
        raise typer.Exit(code=1)

    file_path = get_profiles_dir() / f"{name}.yaml"
    if not file_path.exists():
        console.print(f"{ICON_ERR} Error: Profile '{name}' does not exist.")
        console.print()
        raise typer.Exit(code=1)

    # Request confirmation
    confirm = console.input(
        f"{ICON_ASK} Are you sure you want to delete profile '{name}'? [y/N]: ", markup=False
    ).strip().lower() in [
        "y",
        "yes",
    ]
    if not confirm:
        console.print(f"{ICON_INFO} Deletion cancelled.")
        console.print()
        raise typer.Exit(code=0)
    try:
        file_path.unlink()
        console.print(f"{ICON_OK} Profile '{name}' has been deleted.")
        console.print()
    except Exception as e:
        console.print(f"{ICON_ERR} Error: Failed to delete profile '{name}': {e}")
        console.print()
        raise typer.Exit(code=1)
    finally:
        # List remaining profiles
        ctx.invoke(list)


# Register alias 'del, rm' that point to the same function
profiles.command(name="del", help="Alias for delete", hidden=True)(delete)
profiles.command(name="rm", help="Alias for delete", hidden=True)(delete)


@user.command(help="[bold green]Authenticate[/bold green] user and obtain token")
def auth():
    """Authenticate user and obtain token."""
    if get_token():
        console.print(f"{ICON_OK} User authenticated successfully.")
    else:
        console.print(f"{ICON_ERR} Failed to authenticate user.")
    console.print()


@user.command(help="[bold green]Get[/bold green] user authentication id")
def id():
    """Get user authentication id."""
    user = get_user_id()  # Assume this function extracts user info from token
    if user:
        console.print(f"{ICON_OK} User is authenticated as: {user}")
    else:
        console.print(f"{ICON_ERR} User is not authenticated.")
    console.print()


if __name__ == "__main__":
    sys.exit(app())

# reliafy.py
