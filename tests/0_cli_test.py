# -*- coding: utf-8 -*-
"""Tests for basic CLI function."""
from . import help_check
from . import print_docstring
from . import run_zeigen
from . import working_directory


def test_cli():
    """Test global help function."""
    help_check("global")


@print_docstring()
def test_version(tmp_path):
    """Test version command."""
    with working_directory(tmp_path):
        output = run_zeigen(["--version"])
        assert "version" in output
