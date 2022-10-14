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
    with datadir_mgr.in_tmp_dir(inpathlist=[TABLE_FILE]):
        args = ["--verbose", "list-columns", TABLE_FILE]
        columns = run_zeigen(args)
        assert len(columns.split("\n")) > 3


@print_docstring()
def test_print_cols(datadir_mgr):
    """Test printing select columns."""
    n_lines = 25
    with datadir_mgr.in_tmp_dir(inpathlist=[TABLE_FILE]):
        args = [
            "--verbose",
            "print-columns",
            "--first-n",
            str(n_lines),
            TABLE_FILE,
            "macromolecule",
            "pH",
        ]
        head = run_zeigen(args)
        assert len(head.split("\n")) == n_lines + 2
        args[3] = str(-n_lines)
        tail = run_zeigen(args)
        assert len(tail.split("\n")) == n_lines + 2
        assert head != tail
