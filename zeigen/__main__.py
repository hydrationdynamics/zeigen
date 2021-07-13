# -*- coding: utf-8 -*-
"""Command-line interface and logging configuration."""
# standard-library imports
from importlib import metadata
from typing import Optional

<<<<<<< HEAD
=======
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata

>>>>>>> 3ff9e7431d4be10b20e9d0edd695d48ca135c940
import typer

from .common import APP
from .common import NAME
from .common import STATE
from .find import find

# global constants
unused_cli_funcs = (find,)  # noqa: F841
VERSION: str = metadata.version(NAME)
click_object = typer.main.get_command(APP)  # noqa: F841


def version_callback(value: bool) -> None:
    """Print version info."""
    if value:
        typer.echo(f"{APP.info.name} version {VERSION}")
        raise typer.Exit()


VERSION_OPTION = typer.Option(
    None,
    "--version",
    callback=version_callback,
    help="Print version string.",
)


@APP.callback()
def set_global_state(
    verbose: bool = False,
    quiet: bool = False,
    version: Optional[bool] = VERSION_OPTION,
) -> None:
    """Set global-state variables."""
    if verbose:
        STATE["verbose"] = True
        STATE["log_level"] = "DEBUG"
    elif quiet:
        STATE["log_level"] = "ERROR"
    unused_state_str = f"{version}"  # noqa: F841


def main() -> None:
    """Run the app."""
    APP()
