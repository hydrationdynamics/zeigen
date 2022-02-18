# -*- coding: utf-8 -*-
"""Query PDB for structures."""
# standard library imports
import datetime
import operator
import time
from functools import reduce
from pathlib import Path
from typing import Optional
from typing import Union

import pandas as pd
from loguru import logger
from rcsbsearch import Attr as RCSBAttr  # type: ignore
from rcsbsearch import rcsb_attributes as rcsbsearch_attributes  # type: ignore
from rcsbsearch.search import Terminal  # type: ignore
from statsdict import Stat

from . import rcsb_attributes
from .common import APP
from .common import NAME
from .common import STATS
from .config import read_config

OPERATOR_DICT = {
    "<": operator.lt,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    ">": operator.gt,
}


@APP.command()
def rcsb_attributes_to_py() -> None:
    """Write RCSB attributes list as python code."""
    outfile = "rcsb_attributes.py"
    logger.info(f'Writing RCSB attributes list to "{outfile}".')
    with Path(outfile).open("w") as fp:
        date = datetime.date.today()
        fp.write(f'"""Set of RCSB attributes as of {date}."""\n')
        fp.write("rcsb_attr_set = (\n")
        for attrib in rcsbsearch_attributes:
            fp.write(f'    "{attrib.attribute}",\n')
        fp.write(")\n")


def rcsb_query(
    field: str, op_str: str, val: Union[int, float, str]
) -> Terminal:
    """Convert query specifiers to queries."""
    if field not in rcsb_attributes.rcsb_attr_set:
        raise ValueError(f'Unrecognized RCSB field "{field}"')
    try:
        op = OPERATOR_DICT[op_str]
    except KeyError:
        raise ValueError(
            f'Unrecognized RCSB operator string "{op_str}"'
        ) from None
    return op(RCSBAttr(field), val)


@APP.command()
@STATS.auto_save_and_report
def query(
    set_name: str,
    neutron_only: Optional[bool] = False,
) -> None:
    """Query PDB for structures as defined in config file."""
    config = read_config(NAME)
    extra_queries = [rcsb_query(**e) for e in config.query.extras]
    if neutron_only:
        subtypes = ["neutron"]
    else:
        subtypes = config.query.subtypes
    all_keys = []
    all_types = []
    for subtype in subtypes:
        query_list = [
            rcsb_query(**e) for e in config.query[subtype]
        ] + extra_queries
        combined_query = reduce(operator.iand, query_list)
        start_time = time.time()
        results = list(combined_query())
        n_results = len(results)
        elapsed_time = round(time.time() - start_time, 1)
        logger.info(
            f"RCSB returned {n_results} {subtype} structures in {elapsed_time} s."
        )
        STATS[f"{subtype}_structures"] = Stat(n_results)
        all_keys += results
        all_types += [subtype] * n_results
    STATS["total_structures"] = Stat(len(all_keys))
    df = pd.DataFrame(index=all_keys, data={"type": all_types})
    df.index.name = "PDB"
    df.to_csv(set_name + ".tsv", sep="\t")
