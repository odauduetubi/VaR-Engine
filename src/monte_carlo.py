import numpy as np
import matplotlib.pyplot as plt


def monte_carlo_var(log_returns, weights, portfolio_value=1_000_000, simulations=10_000, horizon=1, confidence_level=0.99):
    weights = np.array(weights)
    mean_returns = log_returns.mean().values
    cov_matrix = log_returns.cov().values

    # Cholesky decomposition for generating correlated random returns
    L = np.linalg.cholesky(cov_matrix)

    simulated_portfolio_returns = []

    for _ in range(simulations):
        # Generate correlated random shocks
        z = np.random.standard_normal(len(weights))
        correlated_shocks = L @ z # @ is the matrix multiplication operator in Python 3.5+

        # Simulate returns for each asset
        simulated_returns = mean_returns + correlated_shocks

        # Portfolio return
        portfolio_return = np.dot(weights, simulated_returns)
        simulated_portfolio_returns.append(portfolio_return)

    simulated_portfolio_returns = np.array(simulated_portfolio_returns)

    mc_var = -np.percentile(simulated_portfolio_returns, (1 - confidence_level) * 100)
    mc_cvar = -simulated_portfolio_returns[simulated_portfolio_returns < -mc_var].mean()

    return {'simulated_returns': simulated_portfolio_returns, 'VaR': mc_var * portfolio_value, 'CVaR': mc_cvar * portfolio_value}





def monte_carlo_paths(log_returns, weights, portfolio_value=1_000_000, simulations=1000, horizon=252):
    weights = np.array(weights)
    mean_returns = log_returns.mean().values
    cov_matrix = log_returns.cov().values

    # Cholesky decomposition for generating correlated random returns
    L = np.linalg.cholesky(cov_matrix)

    all_paths = []

    for _ in range(simulations):
        path = [portfolio_value]
        for t in range(horizon):
            z = np.random.standard_normal(len(weights))
            correlated_shocks = L @ z # @ is the matrix multiplication operator in Python 3.5+
            daily_returns = mean_returns + correlated_shocks
            portfolio_daily_return = np.dot(weights, daily_returns)
            path.append(path[-1] * (1 + portfolio_daily_return))

        all_paths.append(path)

    return np.array(all_paths)