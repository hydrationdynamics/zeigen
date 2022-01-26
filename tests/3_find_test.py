# -*- coding: utf-8 -*-
"""Tests for data ingestion."""
# standard library imports
import sys
from pathlib import Path

import pytest
import sh

from . import help_check
from . import INPUTS
from . import print_docstring
from . import TOML_FILE

# global constants
zeigen = sh.Command("zeigen")
SUBCOMMAND = "find"


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_find(datadir_mgr):
    """Test finding hydrated proton species."""
    with datadir_mgr.in_tmp_dir(
        inpathlist=INPUTS,
        save_outputs=True,
        outscope="module",
    ):
        args = ["--verbose", SUBCOMMAND, TOML_FILE]
        try:
            zeigen(
                args,
                _out=sys.stderr,
            )
        except sh.ErrorReturnCode as errors:
            print(errors)
            pytest.fail("find failed")
        for filestring in ["zeigen_stats.json", "hydrated_waters.tsv"]:
            assert Path(filestring).exists()
