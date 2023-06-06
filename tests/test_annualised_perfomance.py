import pandas as pd
import numpy as np
from helpers import portfolio_calculations as pc


def test_portfolio_annualised_performance():
    # Define test data
    weights = np.array([0.5, 0.5])
    mean_returns = pd.DataFrame({'AAPL': [0.01, 0.02, -0.03, 0.04, -0.05],
                                 'GOOG': [0.02, -0.03, 0.04, -0.05, 0.06]}).mean()
    cov = np.array([[0.01, 0.005], [0.005, 0.02]])
    performance = {'mean_returns': mean_returns, 'cov': cov}

    # Calculate expected returns and volatility
    expected_returns = np.sum(mean_returns * weights) * 252
    expected_volatility = np.sqrt(np.dot(weights.T, np.dot(cov, weights))) * np.sqrt(252)

    # Calculate actual returns and volatility using the function
    actual_returns, actual_volatility = pc.portfolio_annualised_performance(weights, performance)

    # Check that the actual and expected values are equal (within a tolerance)
    assert np.isclose(actual_returns, expected_returns, rtol=1e-6)
    assert np.isclose(actual_volatility, expected_volatility, rtol=1e-6)