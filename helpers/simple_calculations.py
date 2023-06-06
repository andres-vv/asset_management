"""Helper functions for calculating portfolio statistics."""

import datetime
import logging
import math
from typing import Union, Dict

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import config


def calc_assets_perfomance(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """Calculates the daily returns for a DataFrame of asset prices.

    Args:
        df (pd.DataFrame): DataFrame of asset prices.

    Returns:
        pd.DataFrame: DataFrame of daily returns.
    """

    logging.info("Calculating performance for individual assets.")
    assets_perfomance = {}
    # Calculate daily returns
    assets_perfomance['mean_returns'] = df.pct_change().iloc[1:].mean()
    assets_perfomance['cov'] = df.pct_change().iloc[1:].cov()
    assets_perfomance['asset_returns'] = df.pct_change().iloc[1:]

    # Return DataFrame of daily returns
    return assets_perfomance
