"""Module with functions for plotting data."""

import math
from typing import Dict

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

import config


def plot_individual_asset_performance(performance: Dict[str, pd.DataFrame]) -> None:
    """Plots a bar chart of the performance of each asset in the portfolio.

    Args:
        performance (Dict[str, pd.DataFrame]): Dictionary of mean returns and covariance matrix.
    """
    annualized_returns = np.asarray(performance['mean_returns']) * 252
    tickers = [config.TICKER_MAPPING.get(
        ticker, ticker) for ticker in config.TICKERS]
    annualized_stds = np.sqrt(np.diag(performance['cov'])) * np.sqrt(252)

    margin = 2.5 * annualized_stds

    plt.figure(figsize=(12, 6))  # Increase the size of the plot
    plt.errorbar(tickers, annualized_returns, yerr=margin,
                 fmt='o', capsize=5, ecolor='black')
    # Rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(np.arange(
        math.floor(min(annualized_returns-margin)),
        math.ceil(max(annualized_returns+margin)), 0.1), fontsize=12)
    plt.xlabel('Tickers', fontsize=14)
    plt.ylabel('Annualized Returns', fontsize=14)
    plt.title('Individual Asset Performance', fontsize=16)
    plt.grid(axis='y')
    plt.legend(['Annualized Returns'], loc='upper left', fontsize=12)

    # Adjust the bottom margin
    plt.subplots_adjust(bottom=0.2)

    plt.show()


def plot_bar_chart(performance: Dict[str, pd.DataFrame]) -> None:
    """Plots a bar chart with the actual values on top of the bars.

    Args:
        performance (Dict[str, pd.DataFrame]): Dictionary of mean returns and covariance matrix.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    rects = ax.bar(config.TICKERS, np.asarray(performance['mean_returns']) * 252)

    # Add the actual values on top of the bars
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4), textcoords='offset points', ha='center', va='bottom')

    ax.set_title('Individual Asset Performance')
    ax.set_xlabel('xlabel')
    ax.set_ylabel('ylabel')
    plt.show()


def plot_correlation_matrix(performace: Dict[str, pd.DataFrame]) -> None:
    """Plots a heatmap of the correlation matrix of the assets in the portfolio.

    Args:
        performace (Dict[str, pd.DataFrame]): Dictionary of mean returns and covariance matrix.
    """
    covariance_matrix = performace['cov']
    std = np.sqrt(np.diag(covariance_matrix))
    correlation_matrix = covariance_matrix / np.outer(std, std)

    ax = sns.heatmap(
        correlation_matrix,
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True)
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right')
    plt.show()
