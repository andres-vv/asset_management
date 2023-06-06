"""
"""

from typing import List, Dict, Tuple

import numpy as np
import pandas as pd

import config


def portfolio_annualised_performance(weights: np.array, performance: Dict[str, pd.DataFrame])\
        -> Tuple[float, float]:
    """Calculates the annualised performance of a portfolio.

    - Annualised return: the sum of the mean returns of each asset
        multiplied by the weights of each asset, multiplied by 252
        (the number of trading days in a year).
    - Annualised volatility: the square root of the dot product of the transposed
        weights and the dot product of the covariance matrix and the weights,
        multiplied by the square root of 252.

    Args:
        weights (np.array): Array of weights for each asset in the portfolio.
        performance (Dict[str, pd.DataFrame]): Dictionary of mean returns and covariance matrix.

    Returns:
        Tuple(float, float): Tuple of annualised returns and volatility."""
    returns = np.sum(performance['mean_returns']*weights)*252
    std = np.sqrt(np.dot(weights.T,
                         np.dot(performance['cov'], weights))) * np.sqrt(252)
    return returns, std


def portfolio_sharpe_ratio(weights: np.ndarray, performance: Dict[str, np.ndarray]) -> float:
    """Calculates the negative Sharpe ratio for a portfolio
        given its weights, mean returns, covariance matrix, and risk-free rate.

    Args:
        weights (np.ndarray): Array of weights for each asset in the portfolio.
        performance (Dict[str, np.ndarray]): Dictionary of mean returns and covariance
        matrix of the individual assets.

    Returns:
        float: Negative Sharpe ratio of the portfolio.
    """

    # Calculate portfolio variance and return
    p_var, p_ret = portfolio_annualised_performance(weights, performance)

    # Calculate negative Sharpe ratio
    neg_sharpe_ratio = -(p_ret - config.RISK_FREE_RATE) / p_var

    # Return negative Sharpe ratio
    return neg_sharpe_ratio


def portfolio_volatility(weights: np.ndarray, performance: Dict[str, np.ndarray]) -> float:
    """Calculates the volatility of a portfolio given its weights and covariance matrix.

    Args:
        weights (np.ndarray): Array of weights for each asset in the portfolio.
        performance (Dict[str, np.ndarray]): Dictionary of mean returns and covariance
        matrix of the individual assets.

    Returns:
        float: Volatility of the portfolio.
    """
    cov_matrix = performance['cov']
    std = np.sqrt(np.dot(weights.T,
                         np.dot(cov_matrix, weights))) * np.sqrt(252)

    return std


def portfolio_return(weights: np.ndarray, performance: Dict[str, np.ndarray]) -> float:
    """Calculates the return of a portfolio given its weights and mean returns.

    Args:
        weights (np.ndarray): Array of weights for each asset in the portfolio.
        performance (Dict[str, np.ndarray]): Dictionary of mean returns and covariance
        matrix of the individual assets.

    Returns:
        float: Return of the portfolio.
    """
    mean_returns = performance['mean_returns']
    returns = np.sum(mean_returns*weights)*252

    return returns
