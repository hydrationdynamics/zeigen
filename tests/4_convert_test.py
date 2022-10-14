"""Tests for data ingestion."""
# third-party imports
from pathlib import Path

# module imports
from . import TABLE_FILE
from . import help_check
from . import print_docstring
from . import run_zeigen


# global constants
SUBCOMMAND = "parquet-to-tsv"


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_convert(datadir_mgr):
    """Test converting parquet to tsv."""
    with datadir_mgr.in_tmp_dir(
        inpathlist=[TABLE_FILE],
        save_outputs=True,
        outscope="module",
    ):
        args = ["--verbose", SUBCOMMAND, TABLE_FILE]
        run_zeigen(args)
        assert Path("test.tsv").exists()


@print_docstring()
def test_list_cols(datadir_mgr):
    """Test listing column names."""
    with datadir_mgr.in_tmp_dir(
        inpathlist=[TABLE_FILE],
        save_outputs=True,
        outscope="module",
    ):
        args = ["--verbose", "list-columns", TABLE_FILE]
        run_zeigen(args)


@print_docstring()
def test_print_cols(datadir_mgr):
    """Test printing select columns."""
    with datadir_mgr.in_tmp_dir(
        inpathlist=[TABLE_FILE],
        save_outputs=True,
        outscope="module",
    ):
        args = [
            "--verbose",
            "print-columns",
            "--first-n",
            "25",
            TABLE_FILE,
            "macromolecule",
            "pH",
        ]
        run_zeigen(args)
