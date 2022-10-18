"""Base for pytest testing."""
# third-party imports
import contextlib
import copy
import functools
import os
from pathlib import Path
from typing import Callable

import pytest
import sh
from sh import ErrorReturnCode


STATSFILE = "zeigen_stats.json"
TABLE_FILE = "test.parquet"
QUERY_OUTPUTS = ["zeigen.toml", STATSFILE, TABLE_FILE, "test.fa"]


@contextlib.contextmanager
def working_directory(path: str) -> None:
    """Change working directory in context."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def help_check(subcommand: str) -> None:
    """Test help function for subcommand."""
    print(f"Test {subcommand} help.")
    if subcommand == "global":
        help_command = ["--help"]
    else:
        help_command = [subcommand, "--help"]
    try:
        output = sh.zeigen(help_command)
    except ErrorReturnCode as errors:
        print(errors)
        pytest.fail(f"{subcommand} help test failed")
    print(output)
    assert "Usage:" in output
    assert "Options:" in output


def print_docstring() -> Callable:
    """Decorator to print a docstring."""

    def decorator(func: Callable) -> Callable:
        """Define decorator."""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Print docstring and call function."""
            print(func.__doc__)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def run_zeigen(args, envvardict=None):
    """Run zeigen with args."""
    command_string = " ".join(args)
    environ = copy.deepcopy(os.environ)
    environ["ZEIGEN_CONFIG_DIR"] = "."
    if envvardict is not None:
        for k in envvardict.keys():
            environ[k] = envvardict[k]
    try:
        output = sh.zeigen(args, _env=environ)
    except sh.ErrorReturnCode as errors:
        print(errors)
        pytest.fail(f"zeigen {command_string} failed")
    return output
