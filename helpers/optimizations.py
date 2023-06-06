"""Module with optimization functions for different portfolio optimization methods."""

import logging
from typing import Tuple, List, Dict, Callable, Union, Any
from dataclasses import dataclass

import numpy as np
import scipy.optimize as sco

import config
from helpers import portfolio_calculations as pc


@dataclass
class OptimizationResult:
    """Data class for optimization results."""
    weights: np.ndarray
    fun: float
    method: str


def optimize_portfolio(performance: Dict[str, np.ndarray],method: str,
                       add_constraints: List[Dict[str, Any]] = []) \
        -> OptimizationResult:
    """Optimizes a portfolio given its mean returns and covariance matrix.

    Args:
        performance (Dict[str, np.ndarray]): Dictionary of mean returns and covariance matrix.
        method (str): Optimization method to use ('max_sharpe_ratio' or 'min_variance').
        add_constraints (List[Dict[str, Union[str, Callable]]]):
            List of additional constraints to apply to the optimization problem.

    Returns:
        OptimizationResult: Optimized portfolio weights and objective function value.
    """
    logging.info(f"Optimizing portfolio using '{method}' method.")

    num_assets = len(performance['mean_returns'])
    args = (performance)
    bounds = sco.Bounds(np.zeros(num_assets), np.ones(num_assets))
    x0 = num_assets * [1. / num_assets,]
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
    for add_cstr in add_constraints:
        constraints.append(add_cstr)

    try:
        obj_func = config.OPTIMIZATION_CRITERIA[method]
    except KeyError:
        raise ValueError(f"Invalid optimization method '{method}'")

    result = sco.minimize(obj_func,
                          x0=x0,
                          args=args,
                          method='SLSQP',
                          bounds=bounds,
                          constraints=tuple(constraints))

    return OptimizationResult(weights=result.x,
                              fun=result.fun,
                              method=method)


def show_efficient_frontier(mean_returns: np.ndarray, cov_matrix: np.ndarray):
    """Calculates the efficient frontier for a set of expected returns.

    Args:
        mean_returns (np.ndarray): Array of mean returns for each asset.
        cov_matrix (np.ndarray): Covariance matrix of asset returns.
    """
    efficient_frontier = []
    target_returns = np.linspace(0, 0.30, 60)
    for ret in target_returns:
        add_constraints = [{
            'type': 'eq',
            'fun': lambda x: pc.portfolio_return(x, mean_returns) - ret
        }]
        result = optimize_portfolio(
            mean_returns, cov_matrix, 'min_variance', add_constraints)
        # add this tuple = (return, volatility)
        efficient_frontier.append((ret, result.fun))

    # TODO plot efficient frontier
