"""Tests for data ingestion."""
# third-party imports
from copy import deepcopy
from pathlib import Path

# first-party imports
from zeigen.query import delist_responses

# module imports
from . import QUERY_OUTPUTS
from . import STATSFILE
from . import help_check
from . import print_docstring
from . import run_zeigen


SUBCOMMAND = "query"
METADATA_TEST_IDS = ["1STP", "2JEF"]
RESPONSE_SIMPLE = {"a": 1, "b": {"c": 2}, "d": {"e": {"f": 3}}}
RESPONSE_DEPTH = {"a": [1], "b": {"c": [2, 3]}, "d": {"e": {"f": [4, 5, 6]}}}
RESPONSE_MIXED = {
    "a": [{"b": {"c": 2}}, {"b": {"c": 3}}],
    "d": {"e": {"f": [4, 5, 6, 7]}},
}
RESPONSE_HYBRID = {
    "a": [{"b": {"c": [2, 3]}, "d": 1}, {"b": {"c": [12, 13], "d": 2}}],
    "e": {"f": {"g": [4, 5]}},
}

RESPONSE_1STP = {
    "rcsb_id": "1STP",
    "rcsb_entry_info": {
        "diffrn_resolution_high": {"value": 2.6},
        "molecular_weight": 16.75,
        "deposited_atom_count": 1001,
        "deposited_solvent_atom_count": 84,
        "entity_count": 3,
        "polymer_entity_count_protein": 1,
        "deposited_model_count": 1,
        "deposited_polymer_monomer_count": 159,
        "deposited_nonpolymer_entity_instance_count": 1,
        "nonpolymer_entity_count": 1,
    },
    "polymer_entities": [
        {
            "entity_poly": {
                "pdbx_seq_one_letter_code_can": "DPSKDSKAQVSAAEAGITGTWYNQLGSTFIVTAGADGALTGTYESAVGNAESRYVLTGRYDSAPATDGSGTALGWTVAWKNNYRNAHSATTWSGQYVGGAEARINTQWLLTSGTTEANAWKSTLVGHDTFTKVKPSAASIDAAKKAGVNNGNPLDAVQQ"  # noqa: B950
            }
        }
    ],
    "exptl_crystal": [{"density_percent_sol": 73.86, "density_Matthews": 4.71}],
    "exptl_crystal_grow": None,
}
RESPONSE_2JEF = {
    "rcsb_id": "2JEF",
    "rcsb_entry_info": {
        "diffrn_resolution_high": {"value": 2.17},
        "molecular_weight": 51.55,
        "deposited_atom_count": 3615,
        "deposited_solvent_atom_count": 182,
        "entity_count": 6,
        "polymer_entity_count_protein": 1,
        "deposited_model_count": 1,
        "deposited_polymer_monomer_count": 390,
        "deposited_nonpolymer_entity_instance_count": 4,
        "nonpolymer_entity_count": 2,
    },
    "polymer_entities": [
        {
            "entity_poly": {
                "pdbx_seq_one_letter_code_can": "HHHHHHMIVLFVDFDYFYAQVEEVLNPSLKGKPVVVCVFSGRFEDSGAVATANYEARKFGVKAGIPIVEAKKILPNAVYLPMRKEVYQQVSSRIMNLLREYSEKIEIASIDEAYLDISDKVRDYREAYNLGLEIKNKILEKEKITVTVGISKNKVFAKIAADMAKPNGIKVIDDEEVKRLIRELDIADVPGIGNITAEKLKKLGINKLVDTLSIEFDKLKGMIGEAKAKYLISLARDEYNEPIRTRVRKSIGRIVTMKRNSRNLEEIKPYLFRAIEESYYKLDKRIPKAIHVVAVTEDLDIVSRGRTFPHGISKETAYSESVKLLQKILEEDERKIRRIGVRFSKFIEAIGLDKFFDT"  # noqa: B950
            }
        },
        {"entity_poly": {"pdbx_seq_one_letter_code_can": "GGGGGAAGGATTCC"}},
        {"entity_poly": {"pdbx_seq_one_letter_code_can": "TCACNGAATCCTTCCCCC"}},
    ],
    "exptl_crystal": [{"density_percent_sol": 53.08, "density_Matthews": 2.6}],
    "exptl_crystal_grow": [{"pH": 7.4}],
}
RESPONSE_2JEF_REORDERED = {
    "rcsb_id": "2JEF",
    "rcsb_entry_info": {
        "diffrn_resolution_high": {"value": 2.17},
        "molecular_weight": 51.55,
        "deposited_atom_count": 3615,
        "deposited_solvent_atom_count": 182,
        "entity_count": 6,
        "polymer_entity_count_protein": 1,
        "deposited_model_count": 1,
        "deposited_polymer_monomer_count": 390,
        "deposited_nonpolymer_entity_instance_count": 4,
        "nonpolymer_entity_count": 2,
    },
    "exptl_crystal": [{"density_percent_sol": 53.08, "density_Matthews": 2.6}],
    "exptl_crystal_grow": [{"pH": 7.4}],
    "polymer_entities": [
        {
            "entity_poly": {
                "pdbx_seq_one_letter_code_can": "HHHHHHMIVLFVDFDYFYAQVEEVLNPSLKGKPVVVCVFSGRFEDSGAVATANYEARKFGVKAGIPIVEAKKILPNAVYLPMRKEVYQQVSSRIMNLLREYSEKIEIASIDEAYLDISDKVRDYREAYNLGLEIKNKILEKEKITVTVGISKNKVFAKIAADMAKPNGIKVIDDEEVKRLIRELDIADVPGIGNITAEKLKKLGINKLVDTLSIEFDKLKGMIGEAKAKYLISLARDEYNEPIRTRVRKSIGRIVTMKRNSRNLEEIKPYLFRAIEESYYKLDKRIPKAIHVVAVTEDLDIVSRGRTFPHGISKETAYSESVKLLQKILEEDERKIRRIGVRFSKFIEAIGLDKFFDT"  # noqa: B950
            }
        },
        {"entity_poly": {"pdbx_seq_one_letter_code_can": "GGGGGAAGGATTCC"}},
        {"entity_poly": {"pdbx_seq_one_letter_code_can": "TCACNGAATCCTTCCCCC"}},
    ],
}

RESPONSES = (
    {"name": "simple", "response": RESPONSE_SIMPLE, "count": 1},
    {"name": "depth", "response": RESPONSE_DEPTH, "count": 6},
    {"name": "mixed", "response": RESPONSE_MIXED, "count": 8},
    {"name": "hybrid", "response": RESPONSE_HYBRID, "count": 16},
    {"name": "1STP", "response": RESPONSE_1STP, "count": 1},
    {"name": "2JEF", "response": RESPONSE_2JEF, "count": 3},
    {
        "name": "2JEF_reordered",
        "response": RESPONSE_2JEF_REORDERED,
        "count": 3,
    },
)


def test_subcommand_help():
    """Test subcommand help message."""
    help_check(SUBCOMMAND)


@print_docstring()
def test_delist_responses():
    """Test list removal from responses."""
    total_responses = 0
    all_responses = []
    for example in RESPONSES:
        all_responses.append(deepcopy(example["response"]))
        delisted_responses = delist_responses((example["response"],))
        total_responses += example["count"]
        print(
            f"   example {example['name']} returned {len(delisted_responses)} responses"
        )
        try:
            assert len(delisted_responses) == example["count"]
        except AssertionError:
            print(f"{example['name']} in = {all_responses[-1]}", flush=True)
            print(
                f"out {len(delisted_responses)}= {delisted_responses}",
                flush=True,
            )
            raise AssertionError(
                f"Example {example['name']} returned {len(delisted_responses)},"
                f" should have returned {example['count']}"
            ) from None
    all_delisted = delist_responses(tuple(all_responses))
    print(f"   all examples returned {len(all_delisted)} responses\n")
    assert len(all_delisted) == total_responses


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
        outscope="global",
    ):
        args = ["--verbose", SUBCOMMAND, "test"]
        run_zeigen(args)
        for filepath in QUERY_OUTPUTS:
            assert Path(filepath).exists()
