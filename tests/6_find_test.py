"""Tests for data ingestion."""
# third-party imports
from pathlib import Path
from tempfile import TemporaryDirectory

# module imports
from . import help_check
from . import print_docstring
from . import run_zeigen


# global constants
SUBCOMMAND = "water-neighbors"


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_water_neighbors(datadir_mgr):
    """Test finding nearest neighbors of waters."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        with TemporaryDirectory() as cache_dir:
            env_vars = {"RCSB_CACHE_DIR": cache_dir}
            args = ["--verbose", SUBCOMMAND, "5YCE"]
            run_zeigen(args, envvardict=env_vars)
            for filestring in ["5YCE/neighbors.tsv", "5YCE/metadata.json"]:
                assert Path(filestring).exists()
