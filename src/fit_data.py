"""Curve-fitting routines for Incucyte fluorescence and viability data.

Provides three fitting strategies:

* :func:`sigmoid_fit`  — logistic growth model for fluorescence reporter
  traces (ISG expression onset).
* :func:`exponential_fit` — exponential growth model for early-phase
  fluorescence traces.
* :func:`viability_linear_fit` — linear regression on viability
  (confluence) traces from mock-infected control plates.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from statsmodels.tools.eval_measures import rmse


def sigmoid(t: np.ndarray, K: float, tau: float, b: float, c: float) -> np.ndarray:
    """Logistic (sigmoid) function.

    .. math::

        y(t) = \\frac{K}{1 + e^{-b(t - \\tau)}} + c

    Parameters
    ----------
    t : array-like
        Time points.
    K : float
        Carrying capacity (maximum signal amplitude above baseline).
    tau : float
        Inflection point (time of half-maximal induction).
    b : float
        Growth rate (steepness of the sigmoid).
    c : float
        Baseline offset.

    Returns
    -------
    np.ndarray
        Sigmoid values at each time point in *t*.
    """
    return K / (1 + np.exp(-b * (t - tau))) + c


def sigmoid_fit(col: pd.Series) -> pd.Series:
    """Fit a sigmoid to a fluorescence time-series up to its peak.

    The series is truncated at its maximum value before fitting, as the
    post-peak decline is not captured by the logistic model.  Fitting uses
    the Dogleg trust-region algorithm (``method='dogbox'``) from
    :func:`scipy.optimize.curve_fit`.

    Parameters
    ----------
    col : pd.Series
        Time-indexed fluorescence signal for a single well (already smoothed).

    Returns
    -------
    pd.Series
        Fitted parameters and goodness-of-fit metrics with keys:
        ``['c', 'K', 'beta', 'tau', 'r_squared', 'r_squared_adj', 'rmse']``.
        All values are ``np.nan`` if the fit fails or there are too few points.
    """
    _nan_result = pd.Series({
        "c": np.nan,
        "K": np.nan,
        "beta": np.nan,
        "tau": np.nan,
        "r_squared": np.nan,
        "r_squared_adj": np.nan,
        "rmse": np.nan,
    })
    try:
        col = col.dropna().truncate(after=col.idxmax())
        if len(col) <= 4:
            raise ValueError(
                f"Too few data points to fit sigmoid ({len(col)} points, need > 4)."
            )
        K_temp = col.max()
        p0 = [
            col.max(),
            col.index[np.searchsorted(col, K_temp / 2)],
            0.2,
            col.min(),
        ]
        popt, _ = curve_fit(
            sigmoid, col.index, col.values.flatten(), p0, method="dogbox"
        )
        K, tau, beta, c = popt
        fitted_values = sigmoid(col.index, K, tau, beta, c)
        rmse_ = rmse(col.values.flatten(), fitted_values)
        r_squared = r2_score(col.values.flatten(), fitted_values)
        r_squared_adj = 1 - (1 - r_squared) * (len(col) - 1) / (len(col) - len(popt) - 1)
        return pd.Series({
            "c": c,
            "K": K,
            "beta": beta,
            "tau": tau,
            "r_squared": r_squared,
            "r_squared_adj": r_squared_adj,
            "rmse": rmse_,
        })
    except Exception:
        return _nan_result


def exp_func(t: np.ndarray, a: float, b: float) -> np.ndarray:
    """Exponential growth function.

    .. math::

        y(t) = a \\cdot e^{b \\cdot t}

    Parameters
    ----------
    t : array-like
        Time points.
    a : float
        Initial amplitude (value at *t* = 0).
    b : float
        Exponential growth rate.

    Returns
    -------
    np.ndarray
        Exponential values at each time point in *t*.
    """
    return a * np.exp(b * t)


def exponential_fit(col: pd.Series) -> pd.Series:
    """Fit an exponential growth model to a fluorescence time-series.

    Used to characterise the initial growth phase before the signal saturates.
    Initial parameter guesses are derived analytically from the first and last
    non-NaN values of the series.

    Parameters
    ----------
    col : pd.Series
        Time-indexed fluorescence signal for a single well.

    Returns
    -------
    pd.Series
        Fitted parameters and goodness-of-fit metrics with keys:
        ``['starting_GII', 'growth_rate', 'r_squared', 'r_squared_adj']``.
        All values are ``np.nan`` if the fit fails.
    """
    col = col.dropna()
    t = col.index
    y = col.values.flatten()
    p0 = [y[0], np.log(y[-1] / y[0]) / (t[-1] - t[0])]
    try:
        popt, _ = curve_fit(exp_func, t, y, p0)
        r_squared = r2_score(y, exp_func(t, *popt))
        r_squared_adj = (
            1 - (1 - r_squared) * (len(col) - 1) / (len(col) - len(popt) - 1)
        )
        a, b = popt
    except Exception:
        a = b = r_squared = r_squared_adj = np.nan
    return pd.Series({
        "starting_GII": a,
        "growth_rate": b,
        "r_squared": r_squared,
        "r_squared_adj": r_squared_adj,
    })


def viability_linear_fit(col: pd.Series) -> pd.Series:
    """Fit a linear model to a viability (confluence) time-series.

    Used to estimate the basal growth rate and initial confluence of
    mock-infected control wells.

    Parameters
    ----------
    col : pd.Series
        Time-indexed confluence signal (%) for a single mock-infected well.

    Returns
    -------
    pd.Series
        Regression coefficients with keys
        ``['initial_conf', 'growth_rate']``.
    """
    col = col.dropna()
    X = col.index.values.reshape(-1, 1)
    reg = LinearRegression().fit(X, col)
    return pd.Series({
        "initial_conf": reg.intercept_,
        "growth_rate": reg.coef_[0],
    })
