"""Signal processing utilities for Incucyte fluorescence time-series data.

Functions in this module are applied column-wise to raw fluorescence
time-series to remove early-acquisition noise and to smooth the signal
before fitting.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.signal import medfilt, savgol_filter


def remove_initial_noise(col: pd.Series) -> pd.Series | float:
    """Flatten the early noise plateau at the start of a fluorescence trace.

    Incucyte acquisitions often exhibit noisy fluctuations in the first few
    hours before a genuine signal emerges.  This function identifies the
    minimum value within the first 9 hours and replaces all preceding values
    with that minimum, effectively creating a flat baseline up to the true
    signal onset.

    Parameters
    ----------
    col : pd.Series
        Time-indexed fluorescence signal for a single well.

    Returns
    -------
    pd.Series
        Processed signal with early noise replaced by the initial minimum.
        Returns ``np.nan`` if processing fails (e.g. all-NaN input).
    """
    try:
        col = col.dropna()
        # Replace everything up to (and including) the early minimum with that
        # minimum value to suppress pre-signal baseline fluctuations.
        col.loc[: col.loc[:9].idxmin()] = col.loc[:9].min()
        return col
    except Exception:
        return np.nan


def smooth(
    col: pd.Series,
    median_kernel: int = 3,
) -> pd.Series | float:
    """Smooth a fluorescence time-series using median + Savitzky-Golay filters.

    A two-step smoothing pipeline is applied:

    1. **Median filter** (kernel size *median_kernel*) to suppress spike noise.
    2. **Savitzky-Golay filter** (window 7, polynomial order 4) for smooth
       interpolation while preserving the signal shape.

    Negative values introduced by the Savitzky-Golay filter are clipped to
    zero, as negative fluorescence is physically meaningless.

    Parameters
    ----------
    col : pd.Series
        Time-indexed fluorescence signal for a single well.
    median_kernel : int, default 3
        Kernel size for the median filter.  Must be a positive odd integer.

    Returns
    -------
    pd.Series
        Smoothed signal with the same time index as the non-NaN values of
        *col*.  Returns ``np.nan`` if smoothing fails (e.g. too few points).
    """
    try:
        col_clean = col.dropna()
        median_smoothed = medfilt(col_clean, kernel_size=median_kernel)
        savgol_smoothed = savgol_filter(
            median_smoothed, window_length=7, polyorder=4
        )
        # Clip sub-zero artefacts introduced by the Savitzky-Golay filter.
        savgol_smoothed[savgol_smoothed < 0] = 0
        return pd.Series(savgol_smoothed, index=col_clean.index)
    except Exception:
        return np.nan
