"""Module with utility functions."""

import datetime
import logging
import json
from typing import Any, Dict, List

from helpers.optimizations import OptimizationResult
import config


def compare_dates(date_1: str, date_2: str, ticker: str) -> str:
    """Compares two dates and returns the earliest date.

    Args:
        date_1 (str): First date.
        date_2 (str): Second date.
        ticker (str): Ticker of asset.

    Returns:
        str: Earliest date.
    """
    date_format = '%Y-%m-%d'
    datetime_1 = datetime.datetime.strptime(date_1, date_format)
    datetime_2 = datetime.datetime.strptime(date_2, date_format)
    if datetime_1 > datetime_2:
        return date_1, ticker
    else:
        return date_2, ticker


def format_optimization(outcome: OptimizationResult, tickers: List[str]) \
        -> None:
    """Function to format the results of the optimization in
    a more readable format.

    Args:
        outcome (OptimizationResult): OptimizationResult
        tickers (List[str]): List of tickers

    Returns:
        Dict[str, Any]: Formatted results
    """
    # Get the optimized weights
    weights = outcome.weights
    # round to 4 decimal places
    weights = [round(weight, 4) for weight in weights]
    weight_dict = {}
    for ticker, weight in zip(tickers, weights):
        weight_dict[config.TICKER_MAPPING.get(ticker, ticker)] = weight
    # Get the optimized value
    obj_fun = round(outcome.fun, 4)
    # Get the optimization method
    method = outcome.method

    # Format the results
    results = {
        'weights': weight_dict,
        method: obj_fun

    }
    logging.info(
        f"Optimized portfolio weights: {json.dumps(results, indent=4)}")
