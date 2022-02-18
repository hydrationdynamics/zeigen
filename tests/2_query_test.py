# -*- coding: utf-8 -*-
"""Tests for data ingestion."""
# standard library imports
from pathlib import Path

from . import help_check
from . import print_docstring
from . import QUERY_OUTPUTS
from . import run_zeigen

SUBCOMMAND = "query"


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_query(datadir_mgr):
    """Test query of PDB."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = ["--verbose", SUBCOMMAND, "test"]
        run_zeigen(args)
        for filestring in QUERY_OUTPUTS:
            assert Path(filestring).exists()
