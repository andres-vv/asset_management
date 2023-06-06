"""Configuration file for the portfolio optimization."""

from helpers import portfolio_calculations as pc

# Enter your yahoo finance tickers mapping here,
# for easier interpretation of the results.
TICKER_MAPPING = {
    "IE00B4L5Y983": "MSCI_world",
    "VWRD.L": "all_world",
    "MEUD.PA": "europe_600",
    "CD5.PA": "eurostoxx_50",
    "VUSA.L": "sp_500",
    "INRG.L": "clean_energy",
    "SMH": "semicond-uctors",
    "EUCO.PA": "euro_bond",
    "SHYG.L": "hy_euro_bond",
    "EMBE.L": "growth_em_bond",
    "SGLD.L": "gold",
}

# Enter your yahoo finance tickers here
TICKERS = [
    "VWRD.L",
    "MEUD.PA",
    "CD5.PA",
    "VUSA.L",
    "INRG.L",
    "SMH",
    "EUCO.PA",
    "SHYG.L",
    "EMBE.L",
    "SGLD.L"
]

# Enter risk free rate, equal to 10-year US Treasury bond yield
RISK_FREE_RATE = 2.934


OPTIMIZATION_CRITERIA = {
    "max_sharpe_ratio": pc.portfolio_sharpe_ratio,
    "min_variance": pc.portfolio_volatility,
}
