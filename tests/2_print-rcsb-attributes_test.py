# -*- coding: utf-8 -*-
"""Tests for creating list of RCSB attributes."""
import pytest
import sh

from . import help_check
from . import print_docstring

# global constants
zeigen = sh.Command("zeigen")
SUBCOMMAND = "print-rcsb-attributes"
TEST_ATTRIBUTES = [
    "pdbx_struct_special_symmetry.PDB_model_num",
    "rcsb_entry_info.diffrn_resolution_high.value",
    "entity_poly.pdbx_seq_one_letter_code_can",
    "rcsb_polymer_entity.pdbx_description",
    "rcsb_uniprot_alignments.core_entity_alignments.core_entity_identifiers.entity_id",
]
KNOWN_ATTRIBUTES = 1792


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_print_rcsb_attributes(datadir_mgr):
    """Test query of PDB."""
    with datadir_mgr.in_tmp_dir(
        save_outputs=True,
        outscope="module",
    ):
        args = ["--verbose", SUBCOMMAND]
        try:
            output = zeigen(
                args,
            )
        except sh.ErrorReturnCode as errors:
            print(errors)
            pytest.fail("print-rcsb-attributes failed")
        attr_list = str(output)[0:-1].split("\n")
        n_attr = len(attr_list)  # should only get longer
        assert n_attr >= KNOWN_ATTRIBUTES
        print(f"{n_attr} attributes listed ({KNOWN_ATTRIBUTES} at last def)")
        for attr in TEST_ATTRIBUTES:
            assert attr in attr_list
