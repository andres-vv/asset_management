# Asset Allocation by Markowitz Portfolio Theory and Variants

## Setup
Clone this repository by running following command in your terminal:
```
git clone https://github.com/andres-vv/asset_management.git
```
Next go into the directory and install and create a virtual environment:
```
python3 -m venv .venv
source .venv/bin/activate
```

Finally install the requirements:
```
pip install -r requirements.txt
```
## Usage
This repository can be used to determine an optimal allocation of assets in a given portfolio. The weight distribution can be optimized according to different strategies. The following strategies are implemented:
- Minimal Variance of the portfolio
- Maximal Sharpe Ratio of the portfolio
- Weighted Average between Minimal Variance and Maximal Return
- Minimize Variance for given Target Return

Before you run the code, some custom parameters must be specified in the `config.py` file. The following parameters can be set:
- `TICKERS`: list of tickers of assets in the portfolio, use tickers from [Yahoo Finance](https://finance.yahoo.com/).
- `TICKER_MAPPING`: mapping of tickers to asset names, for more readable output.
- `RISK FREE RATE`: risk free rate, equals the Euro-short term rate (€STR) [Source](https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/index.en.html)
- `TARGET_RETURN`: target return for the optimization strategy `Minimize Variance for given Target Return`
- `VOLATILITY_WEIGHT`: weight of volatility in the optimization strategy `Weighted Average between Minimal Variance and Maximal Return`.

Once all parameters are set, the code can be run.
To run code, run the following command in your terminal:
```
python main.py --optimize <strategy> --visuals 
```

Run `python main.py --help` to see all available options.

## In-depth strategy description
### Minimal Variance
In this strategy, the weights are chosen to minimize the variance of the portfolio. This is done by looking at the covariance matrix of all the assets in the porfolio.

### Maximal Sharpe Ratio
In this strategy, the weights are chosen to maximize the Sharpe Ratio of the portfolio. The Sharpe Ratio is defined as the ratio of the expected return of the portfolio minus the risk free rate and the volatility of the portfolio. The expected return is calculated as the weighted average of the expected returns of the assets in the portfolio. The volatility is calculated as the square root of the weighted average of the covariance matrix of the assets in the portfolio.

### Weighted Average between Minimal Variance and Maximal Return
In this strategy, the weights are chose to minimize the following equation:

<img src= "https://latex.codecogs.com/svg.image?{\color{White}&space;objective\_function&space;=&space;(-1&space;*&space;r&space;*&space;port\_return)&space;&plus;&space;((1-r)&space;*&space;port\_volatility)}&space;" />

The constant `r` determines the weighting. If `r=1`, the return of the portfolio is maximized. If `r=0`, the volatility of the portfolio is minimized. If `r=0.5`, the return and volatility are weighted equally.

### Minimize Variance for given Target Return
In this strategy, the weights are chosen to minimize the variance of the portfolio for a given target return. This target return can be specified in the config file. 
## TODO:
- enhance visualization, make one plot with subplots
- write tests for all cases
- add bar chart of asset returns with performance on top.
- add generated portfolios to plot efficient frontier