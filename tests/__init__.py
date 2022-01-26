# -*- coding: utf-8 -*-
"""Base for pytest testing."""
# standard library imports
import contextlib
import functools
import os
from pathlib import Path
from typing import Callable

import pytest
import sh
from sh import ErrorReturnCode

# third-party imports

# global constants
TOML_FILE = "config.toml"
INPUTS = [TOML_FILE]


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


def run_zeigen(args, component):
    """Run zeigen with args."""
    command_string = " ".join(args)
    print(f"Testing {component} with" + f'"svange {command_string}"')
    try:
        sh.zeigen(args)
    except ErrorReturnCode as errors:
        print(errors)
        pytest.fail(f"{component} failed")
