# -*- coding: utf-8 -*-
"""Tests for data ingestion."""
# standard library imports
from pathlib import Path

from . import help_check
from . import print_docstring
from . import QUERY_OUTPUTS
from . import run_zeigen
from . import STATSFILE

SUBCOMMAND = "query"
METADATA_TEST_IDS = ["1STP", "2JEF"]


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_metadata(datadir_mgr):
    """Test metadata return from RCSB."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [
            "--verbose",
            "rcsb-metadata",
            "--show-frame",
        ] + METADATA_TEST_IDS
        output = run_zeigen(args)
        for id in METADATA_TEST_IDS:
            assert id in output


@print_docstring()
def test_simple_query(datadir_mgr):
    """Test query of PDB without metadata."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [
            "--verbose",
            SUBCOMMAND,
            "--neutron-only",
            "--query-only",
            "test",
        ]
        run_zeigen(args)
        assert Path(STATSFILE).exists()


@print_docstring()
def test_full_query(datadir_mgr):
    """Test query of PDB with metadata."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = ["--verbose", SUBCOMMAND, "test"]
        run_zeigen(args)
        for filepath in QUERY_OUTPUTS:
            assert Path(filepath).exists()
