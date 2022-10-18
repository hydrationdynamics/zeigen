"""Tests for data ingestion."""
from pathlib import Path
from tempfile import TemporaryDirectory

# module imports
from . import help_check
from . import print_docstring
from . import run_zeigen


# global constants
SUBCOMMAND = "get-structure"


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_get_pdb(datadir_mgr):
    """Test download of PDB structure file."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [SUBCOMMAND, "5YCE"]
        output = run_zeigen(args)
        assert Path(str(output).strip()).exists()


@print_docstring()
def test_dl_to_envvar_dir(datadir_mgr):
    """Test download to a envvar-specified dir."""
    with datadir_mgr.in_tmp_dir():
        with TemporaryDirectory() as cache_dir:
            dl_file_path = Path(cache_dir) / "5YCE.pdb"
            args = [SUBCOMMAND, "5YCE"]
            env_vars = {"RCSB_CACHE_DIR": cache_dir}
            run_zeigen(args, envvardict=env_vars)
            assert dl_file_path.exists()


@print_docstring()
def test_get_cif(datadir_mgr):
    """Test download of CIF structure file."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [SUBCOMMAND, "--file-type", "cif", "5YCE"]
        output = run_zeigen(args)
        assert Path(str(output).strip()).exists()


@print_docstring()
def test_get_bcif(datadir_mgr):
    """Test download of BCIF structure file."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [SUBCOMMAND, "--file-type", "bcif", "5YCE"]
        output = run_zeigen(args)
        assert Path(str(output).strip()).exists()


@print_docstring()
def test_get_xml(datadir_mgr):
    """Test download of XML structure file."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [SUBCOMMAND, "--file-type", "xml", "5YCE"]
        output = run_zeigen(args)
        assert Path(str(output).strip()).exists()


@print_docstring()
def test_get_xml_header(datadir_mgr):
    """Test download of XML header file."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [SUBCOMMAND, "--file-type", "xml-header", "5YCE"]
        output = run_zeigen(args)
        assert Path(str(output).strip()).exists()


@print_docstring()
def test_get_pdb_assembly(datadir_mgr):
    """Test download of PDB biological assembly file."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [SUBCOMMAND, "--file-type", "assembly-pdb", "5YCE"]
        output = run_zeigen(args)
        assert Path(str(output).strip()).exists()


@print_docstring()
def test_get_cif_assembly(datadir_mgr):
    """Test download of CIF biological assembly file."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [SUBCOMMAND, "--file-type", "assembly-cif", "5YCE"]
        output = run_zeigen(args)
        assert Path(str(output).strip()).exists()


@print_docstring()
def test_get_bcif_assembly(datadir_mgr):
    """Test download of BCIF biological assembly file."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = [SUBCOMMAND, "--file-type", "assembly-bcif", "5YCE"]
        output = run_zeigen(args)
        assert Path(str(output).strip()).exists()
