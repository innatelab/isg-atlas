"""Functions for reading and parsing Incucyte live-cell imaging export files.

The Incucyte software exports measurements as tab-separated .txt files with
6 header rows. This module provides helpers for loading fluorescence reporter
and cell-viability data and structuring them as multi-index pandas DataFrames
for downstream analysis.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.virus2mock import virus2mock


def read_incucyte_txt_file(txt_file_path: str | Path) -> pd.DataFrame:
    """Read a single Incucyte .txt export and return a tidy DataFrame.

    Skips the 6-row file header, drops the 'Date Time' column, and sets
    elapsed time (hours) as the index. Comma-formatted decimals are
    normalised to dots, and empty-string entries are replaced with NaN.

    Parameters
    ----------
    txt_file_path : str or Path
        Path to the Incucyte-exported .txt file.

    Returns
    -------
    pd.DataFrame
        DataFrame indexed by elapsed time (hours) with well IDs as columns.
    """
    df = pd.read_csv(
        txt_file_path,
        skiprows=6,
        decimal=",",
        sep="\t",
    ).drop(["Date Time"], axis=1).set_index("Elapsed")

    # Some columns are not parsed as numeric and escape the decimal=',' option;
    # isolated spaces (empty wells) are also replaced with NaN.
    df = df.replace(",", ".", regex=True).replace(" ", np.nan).astype(float)
    return df


def read_flrsc_data(
    flrsc_path: str | Path,
    id2virus: dict[str, str],
) -> pd.DataFrame:
    """Load all fluorescence reporter files and return a multi-index DataFrame.

    Each file encodes a single virus / set / biological-replicate combination
    in its filename (e.g. ``V1_S2_R3.txt``). The corresponding mock-plate ID
    is looked up in :data:`src.virus2mock.virus2mock`.

    Parameters
    ----------
    flrsc_path : str or Path
        Directory containing the Incucyte fluorescence .txt files.
    id2virus : dict[str, str]
        Mapping from numeric virus ID string (e.g. ``'1'``) to a descriptive
        virus name (e.g. ``'SARS-CoV-2'``).

    Returns
    -------
    pd.DataFrame
        Multi-index DataFrame with levels
        ``['virus', 'set', 'bio_rep', 'mock_plate_id', 'knockout']``.
    """
    flrsc_txt_files = os.listdir(flrsc_path)
    dfs = []
    for flrsc_txt_file in flrsc_txt_files:
        # Extract IDs from filename; use \d+ to support multi-digit numbers.
        virus_plate_id = Path(flrsc_txt_file).stem
        virus_id, set_, bio_rep = re.match(
            r"V(\d+)_S(\d+)_R(\d+)", virus_plate_id
        ).groups()
        virus = id2virus[virus_id]
        mock_plate_id = virus2mock.get(f"V{virus_id}_S{set_}_R{bio_rep}", np.nan)

        flrsc_df = read_incucyte_txt_file(flrsc_path / flrsc_txt_file)
        flrsc_df.columns = pd.MultiIndex.from_product(
            [[virus], [set_], [bio_rep], [mock_plate_id], flrsc_df.columns],
            names=["virus", "set", "bio_rep", "mock_plate_id", "knockout"],
        )
        dfs.append(flrsc_df)

    df = pd.concat(dfs, axis=1).sort_index(axis=1, ascending=True).sort_index()
    return df


def read_viability_data(viability_path: str | Path) -> pd.DataFrame:
    """Load all viability (mock) files and return a multi-index DataFrame.

    Files are expected to follow the naming convention ``V0_S<set>_R<rep>.txt``
    where ``V0`` denotes mock-infected (uninfected) control plates.

    Parameters
    ----------
    viability_path : str or Path
        Directory containing the Incucyte viability .txt files.

    Returns
    -------
    pd.DataFrame
        Multi-index DataFrame with levels ``['mock_plate_id', 'knockout']``.
    """
    txt_files = sorted(os.listdir(viability_path))
    dfs = []
    for txt_file in txt_files:
        mock_plate_id = Path(txt_file).stem
        set_, bio_rep = re.match(r"V0_S(\d+)_R(\d+)", mock_plate_id).groups()

        df = read_incucyte_txt_file(viability_path / txt_file)
        df.columns = pd.MultiIndex.from_product(
            [[mock_plate_id], df.columns],
            names=["mock_plate_id", "knockout"],
        )
        dfs.append(df)

    df = pd.concat(dfs, axis=1).sort_index(axis=1, ascending=True)
    return df


def split_good_bad_runs(
    df: pd.DataFrame,
    data_format: str = "long",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Partition a DataFrame into usable and all-NaN runs.

    A run is considered 'bad' when every value in its row (long format) or
    column (wide format) is NaN, which typically indicates a failed imaging
    well or acquisition error.

    Parameters
    ----------
    df : pd.DataFrame
        Input data to partition.
    data_format : {'long', 'wide'}, default 'long'
        Orientation of the data.  ``'long'`` treats rows as runs;
        ``'wide'`` treats columns as runs.

    Returns
    -------
    good_runs : pd.DataFrame
        Subset of *df* with all-NaN rows/columns removed.
    bad_runs : pd.DataFrame
        Subset of *df* containing only the all-NaN rows/columns.
    """
    if data_format == "long":
        bad_runs = df.loc[df.isna().all(axis=1), :]
        good_runs = df.drop(bad_runs.index, axis=0)
    else:
        bad_runs = df.loc[:, df.isna().all(axis=0)]
        good_runs = df.drop(bad_runs.columns, axis=1)
    return good_runs, bad_runs
