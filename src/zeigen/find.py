"""Find hydrated waters in structure."""
# third-party imports
import pandas as pd
from loguru import logger
from statsdict import Stat  # type: ignore

# module imports
from .common import APP
from .common import NAME
from .common import STATS
from .config import read_config


@APP.command()
def water_neighbors(rcsb_id: str) -> None:
    """Find neighbors of waters in structure file."""
    conf = read_config(NAME)
    find_params = conf["find"]
    logger.info(f"find params={find_params}")
    output = "hydrated_waters.tsv"
    logger.info(f"writing file {output}")
    df = pd.DataFrame({"A": [1, 2, 3]})
    df.to_csv(output, sep="\t")
