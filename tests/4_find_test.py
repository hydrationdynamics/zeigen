"""Tests for data ingestion."""
# third-party imports
from pathlib import Path

# module imports
from . import help_check
from . import print_docstring
from . import run_zeigen

# global constants
SUBCOMMAND = "find"


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_find(datadir_mgr):
    """Test finding hydrated proton species."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = ["--verbose", SUBCOMMAND, "test"]
        run_zeigen(args)
        for filestring in ["zeigen_stats.json", "hydrated_waters.tsv"]:
            assert Path(filestring).exists()
