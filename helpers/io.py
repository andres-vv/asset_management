"""Module with helper functions for input/output operations."""

import logging
import datetime

import pandas as pd
import yfinance as yf

from helpers import simple_calculations as sc
from helpers import utils
import config


def fetch_tickers(ticker_list: list) -> pd.DataFrame:
    """Fetches data for a list of tickers from Yahoo Finance.

    Args:
        ticker_list (list): List of tickers to fetch data for.

    Returns:
        pd.DataFrame: DataFrame with data for all tickers.
    """
    df = pd.DataFrame()
    logging.info(
        f"Fetching data for {len(ticker_list)} tickers from Yahoo Finance.")
    earliest = '1980-01-01'
    for ticker in ticker_list:
        ticker_yf = yf.Ticker(ticker)
        df_ticker = ticker_yf.history(period='max')['Close']
        # Format index to YYYY-MM-DD
        df_ticker.index = df_ticker.index.strftime('%Y-%m-%d')
        # determine earliest date
        last, last_ticker = utils.compare_dates(
            df_ticker.index[0], earliest, ticker)
        df[config.TICKER_MAPPING[ticker]] = df_ticker
    # Remove any rows that contain NaN values
    df.dropna(inplace=True)
    logging.info(f"Last date was {last} for {config.TICKER_MAPPING[last_ticker]}. "
                 f"This date will be used as the start for benchmarking and optimization.")

    # Return DataFrame
    return df
