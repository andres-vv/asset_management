import matplotlib
import pandas as pd
from pandas_datareader import data as wb
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.optimize as sco
import yfinance as yf
import datetime
import sys

from helpers import io
from helpers import simple_calculations
import config

# plt.style.use('fivethirtyeight')
# np.random.seed(777)
# pd.set_option('display.max_columns', None)

# Geef aandelen in
tickers = ["VWRD.L", "MEUD.PA", "CD5.PA", "VUSA.L",
           "INRG.L", "SMH", "EUCO.PA", "SHYG.L", "EMBE.L", "SGLD.L"]

# Geef target return in
target_return = 0.1

assets = io.fetch_tickers(tickers)
assets_perfomance = simple_calculations.calc_assets_perfomance(assets)

for _, value in assets_perfomance.items():
    print(type(value))




# PLOT STOCK PRICES OVER TIME
# plt.figure(figsize=(14, 7))
# for c in table.columns.values:
#     plt.plot(table.index, table[c], lw=3, alpha=0.8,label=c)
# plt.legend(loc='upper left', fontsize=12)
# plt.ylabel('Price in Dollar')
# plt.show()

# PLOT DAILY RETURNS
# returns = table.pct_change()
# plt.figure(figsize=(14, 7))
# for c in returns.columns.values:
#     plt.plot(returns.index, returns[c], lw=3, alpha=0.8,label=c)
# plt.legend(loc='upper right', fontsize=12)
# plt.ylabel('Daily Returns in %')
# plt.show()


# # CALCULATE PORTFOLIO PEFORMANCE
# def portfolio_annualised_performance(weights, mean_returns, cov_matrix):
#     returns = np.sum(mean_returns*weights)*252
#     std = np.sqrt(np.dot(weights.T, np.dot(
#         cov_matrix, weights))) * np.sqrt(252)
#     return std, returns

# # GENERATE RANDOM PORTOLIOS


# returns = table.pct_change()
# print(returns.head())
# mean_returns = returns.mean()
# cov_matrix = returns.cov()
# num_portfolios = 25000
# risk_free_rate = 0.0013

# DISPLAY GENERATED PORTFOLIOS + MIN VARIANCE & MAX SHARP RATIO


def display_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate):
    results, weights = random_portfolios(
        num_portfolios, mean_returns, cov_matrix, risk_free_rate)

    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
    col_names = [config.ticker_mapping[i] for i in table.columns]
    max_sharpe_allocation = pd.DataFrame(
        weights[max_sharpe_idx], index=col_names, columns=['allocation'])
    max_sharpe_allocation.allocation = [
        round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    min_vol_idx = np.argmin(results[0])
    sdp_min, rp_min = results[0, min_vol_idx], results[1, min_vol_idx]
    min_vol_allocation = pd.DataFrame(
        weights[min_vol_idx], index=col_names, columns=['allocation'])
    min_vol_allocation.allocation = [
        round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    # Text Output
    print("-" * 80)
    print("Maximum Sharpe Ratio Portfolio Allocation (GENERATION)\n")
    print("Annualised Return:", round(rp, 2))
    print("Annualised Volatility:", round(sdp, 2))
    print("\n")
    print(max_sharpe_allocation)
    print("-" * 80)
    print("Minimum Volatility Portfolio Allocation (GENERATION)\n")
    print("Annualised Return:", round(rp_min, 2))
    print("Annualised Volatility:", round(sdp_min, 2))
    print("\n")
    print(min_vol_allocation)
    # Plotting
    plt.figure(figsize=(10, 7))
    plt.scatter(results[0, :], results[1, :], c=results[2, :],
                cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar()
    plt.scatter(sdp, rp, marker='*', color='r',
                s=500, label='Maximum Sharpe ratio')
    plt.scatter(sdp_min, rp_min, marker='*', color='g',
                s=500, label='Minimum volatility')
    plt.title(
        'Simulated Portfolio Optimization based on Efficient Frontier (GENERATED)')
    plt.xlabel('Annualised Volatility')
    plt.ylabel('Annualised Returns')
    plt.legend(labelspacing=0.8)
    # plt.show()


display_simulated_ef_with_random(
    mean_returns, cov_matrix, num_portfolios, risk_free_rate)

# MAXIMIZE SHARPE RATIO AS OPTIMALIZATION PROBLEM


# def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
#     p_var, p_ret = portfolio_annualised_performance(
#         weights, mean_returns, cov_matrix)
#     return -(p_ret - risk_free_rate) / p_var


# def max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate):
#     num_assets = len(mean_returns)
#     args = (mean_returns, cov_matrix, risk_free_rate)
#     constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
#     bound = (0.0, 1.0)
#     bounds = tuple(bound for asset in range(num_assets))
#     result = sco.minimize(neg_sharpe_ratio, num_assets*[1./num_assets,], args=args,
#                           method='SLSQP', bounds=bounds, constraints=constraints)
#     return result

# MINIMIZE PORTFOLIO VARIANCE AS OPTIMALIZATION PROBLEM


def portfolio_volatility(weights, mean_returns, cov_matrix):
    return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]


def min_variance(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0, 1.0)
    bounds = tuple(bound for asset in range(num_assets))

    result = sco.minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)

    return result

# CALCULATE THE EFFICIENT FRONTIER OF PORTFOLIOS


def efficient_return(mean_returns, cov_matrix, target):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def portfolio_return(weights):
        return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[1]

    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for asset in range(num_assets))
    result = sco.minimize(portfolio_volatility, num_assets*[
                          1./num_assets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result


def efficient_frontier(mean_returns, cov_matrix, returns_range):
    efficients = []
    for ret in returns_range:
        efficients.append(efficient_return(mean_returns, cov_matrix, ret))
    return efficients

# PLOT ALL: GENERATED PORTFOLIOS + OPTIMIZED PORTFOLIOS + EFFICIENT FRONTIER


def display_calculated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate):
    results, _ = random_portfolios(
        num_portfolios, mean_returns, cov_matrix, risk_free_rate)

    max_sharpe = max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate)
    sdp, rp = portfolio_annualised_performance(
        max_sharpe['x'], mean_returns, cov_matrix)
    col_names = [config.ticker_mapping[i] for i in assets]
    max_sharpe_allocation = pd.DataFrame(
        max_sharpe.x, index=col_names, columns=['allocation'])
    max_sharpe_allocation.allocation = [
        round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    min_vol = min_variance(mean_returns, cov_matrix)
    sdp_min, rp_min = portfolio_annualised_performance(
        min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(
        min_vol.x, index=col_names, columns=['allocation'])
    min_vol_allocation.allocation = [
        round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    # TEXT OUTPUT
    print("-" * 80)
    print("Maximum Sharpe Ratio Portfolio Allocation (OPTIMALIZATION)\n")
    print("Annualised Return:", round(rp, 2))
    print("Annualised Volatility:", round(sdp, 2))
    print("\n")
    print(max_sharpe_allocation)
    print("-" * 80)
    print("Minimum Volatility Portfolio Allocation (OPTIMALIZATION)\n")
    print("Annualised Return:", round(rp_min, 2))
    print("Annualised Volatility:", round(sdp_min, 2))
    print("\n")
    print(min_vol_allocation)

    # PLOTTING
    plt.figure(figsize=(10, 7))
    plt.scatter(results[0, :], results[1, :], c=results[2, :],
                cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar()
    plt.scatter(sdp, rp, marker='*', color='r',
                s=500, label='Maximum Sharpe ratio')
    plt.scatter(sdp_min, rp_min, marker='*', color='g',
                s=500, label='Minimum volatility')

    target = np.linspace(rp_min, np.max(results[1, :]), 50)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)
    plt.plot([p['fun'] for p in efficient_portfolios], target, linestyle='-.', color='black',
             label='efficient frontier')
    plt.title(
        'Calculated Portfolio Optimization based on Efficient Frontier (OPTIMIZED°')
    plt.xlabel('annualised volatility')
    plt.ylabel('annualised returns')
    plt.legend(labelspacing=0.8)
    plt.show()


display_calculated_ef_with_random(
    mean_returns, cov_matrix, num_portfolios, risk_free_rate)

# PLOT EFFICIENT FRONTIER WITH INDIVIDUAL STOCKS


def display_ef_with_selected(mean_returns, cov_matrix, risk_free_rate):
    results, _ = random_portfolios(
        num_portfolios, mean_returns, cov_matrix, risk_free_rate)

    max_sharpe = max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate)
    sdp, rp = portfolio_annualised_performance(
        max_sharpe['x'], mean_returns, cov_matrix)
    col_names = [config.ticker_mapping[i] for i in table.columns]
    max_sharpe_allocation = pd.DataFrame(
        max_sharpe.x, index=col_names, columns=['allocation'])
    max_sharpe_allocation.allocation = [
        round(i * 100, 2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T

    min_vol = min_variance(mean_returns, cov_matrix)
    sdp_min, rp_min = portfolio_annualised_performance(
        min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(
        min_vol.x, index=col_names, columns=['allocation'])
    min_vol_allocation.allocation = [
        round(i * 100, 2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T

    an_vol = np.std(returns) * np.sqrt(252)
    an_rt = mean_returns * 252

    # TEXT OUTPUT
    print("-" * 80)
    print("Maximum Sharpe Ratio Portfolio Allocation\n")
    print("Annualised Return:", round(rp, 2))
    print("Annualised Volatility:", round(sdp, 2))
    print("\n")
    print(max_sharpe_allocation)
    print("-" * 80)
    print("Minimum Volatility Portfolio Allocation\n")
    print("Annualised Return:", round(rp_min, 2))
    print("Annualised Volatility:", round(sdp_min, 2))
    print("\n")
    print(min_vol_allocation)
    print("-" * 80)
    print("Individual Stock Returns and Volatility\n")
    for i, txt in enumerate(col_names):
        print(txt, ":", "annuaised return", round(
            an_rt[i], 2), ", annualised volatility:", round(an_vol[i], 2))
    print("-" * 80)

    # PLOTTING
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(an_vol, an_rt, marker='o', s=200)

    for i, txt in enumerate(table.columns):
        ax.annotate(txt, (an_vol[i], an_rt[i]), xytext=(
            10, 0), textcoords='offset points')
    ax.scatter(sdp, rp, marker='*', color='r',
               s=500, label='Maximum Sharpe ratio')
    ax.scatter(sdp_min, rp_min, marker='*', color='g',
               s=500, label='Minimum volatility')

    target = np.linspace(rp_min, 0.30, 50)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)
    ax.plot([p['fun'] for p in efficient_portfolios], target,
            linestyle='-.', color='black', label='efficient frontier')
    ax.set_title('Portfolio Optimization with Individual Stocks (OPTIMIZED°')
    ax.set_xlabel('annualised volatility')
    ax.set_ylabel('annualised returns')
    ax.legend(labelspacing=0.8)
    plt.show()


display_ef_with_selected(mean_returns, cov_matrix, risk_free_rate)

# OUTPUT FOR TARGET RETURN


def efficient_target_return(target):
    result = efficient_return(mean_returns, cov_matrix, target)
    weight = result.x
    col_names = [config.ticker_mapping[i] for i in table.columns]
    result = pd.DataFrame(result.x, index=col_names,
                          columns=['allocation'])
    result.allocation = [round(i * 100, 2) for i in result.allocation]
    result = result.T

    def portfolio_return(weights):
        return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[1]

    def portfolio_volatility(weights):
        return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]

    # TEXT OUTPUT
    print("Minimum Volatility for Target return\n")
    print("Annualised Return:", round(portfolio_return(weight), 2))
    print("Annualised Volatility:", round(portfolio_volatility(weight), 2))
    print("\n")
    print(result)
    print("-" * 80)


efficient_target_return(target_return)
