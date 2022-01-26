# -*- coding: utf-8 -*-
"""Tests for creating list of RCSB attributes."""
# standard library imports
import sys
from pathlib import Path

import pytest
import sh

from . import help_check
from . import print_docstring

# from zeigen.rcsb_attributes import rcsb_attr_set as old_attr_set

# global constants
zeigen = sh.Command("zeigen")
SUBCOMMAND = "rcsb-attributes-to-py"


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_rcsb_attributes_to_py(datadir_mgr):
    """Test query of PDB."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = ["--verbose", SUBCOMMAND]
        try:
            zeigen(
                args,
                _out=sys.stderr,
            )
        except sh.ErrorReturnCode as errors:
            print(errors)
            pytest.fail("rcsb-attributes-to-py failed")
        for filestring in ["rcsb_attributes.py"]:
            assert Path(filestring).exists()
        # from . import rcsb_attributes
        # assert old_attr_list == rcsb_attributes.rcsb_attr_set
