import numpy as np
from helpers import portfolio_calculations as pc


def test_portfolio_volatility():
    # Define test data
    weights = np.array([0.5, 0.5])
    cov_matrix = np.array([[0.01, 0.005], [0.005, 0.02]])

    # Calculate expected volatility
    expected_volatility = np.sqrt(np.dot(weights.T,
                                         np.dot(cov_matrix, weights))) * np.sqrt(252)
    # Calculate actual volatility using the function
    actual_volatility = pc.portfolio_volatility(weights, cov_matrix)
    # Check that the actual and expected values are equal (within a tolerance)
    assert np.isclose(actual_volatility, expected_volatility, rtol=1e-6)
