"""Main module that optimizes assets allocation based upon specified optimization criteria."""""
import argparse
import logging

from helpers import io
from helpers import simple_calculations as sc
from helpers.visualization import plot_functions as pf
from helpers import optimizations as opt
from helpers import utils
import config

logging.basicConfig(level=logging.INFO)
parser = argparse.ArgumentParser(description='Define optimization parameters.',
                                 prog='Stocks Portfolio Optimization',
                                 epilog='Shout-out to Andreiro')
parser.add_argument('--optimize', '-o', default='min_variance',
                    choices=config.OPTIMIZATION_CRITERIA.keys(),
                    help='This argument determines your optimization strategy.')
parser.add_argument('--visuals', '-v', action='store_true',
                    help='Add this argument to show plots.')
known_args, _ = parser.parse_known_args()

if __name__ == '__main__':
    logging.info(f"Optimizing portfolio based upon {known_args.optimize}.")
    assets = io.fetch_tickers(config.TICKERS)
    assets_perfomance = sc.calc_assets_perfomance(assets)
    optimized_portfolio = opt.optimize_portfolio(
        assets_perfomance, known_args.optimize)
    utils.format_optimization(optimized_portfolio, assets_perfomance)

    if known_args.visuals:
        logging.info(f"Showing plots...")
        pf.plot_individual_asset_performance(assets_perfomance)
        pf.plot_bar_chart(assets_perfomance)
        pf.plot_correlation_matrix(assets_perfomance)
