import pandas as pd
import numpy as np
from scipy import stats

log_returns = pd.read_csv('../data/log_returns.csv', index_col=0, parse_dates=True)
weights = np.array([0.30, 0.25, 0.20, 0.15, 0.10])

portfolio_returns = log_returns.dot(weights)

# We define some risk metrics functions 
def portfolio_returns(log_returns, weights):
    return log_returns.dot(weights)

def portfolio_stats(log_returns, weights):
    w = np.array(weights)
    mean_returns = log_returns.mean()
    cov_matrix = log_returns.cov()
    port_return = np.dot(w, mean_returns) * 252  # Annualize the return
    port_volatility = np.sqrt(np.dot(w.T, np.dot(cov_matrix * 252, w)))  # Annualize the volatility
    
    if port_volatility == 0:
        raise ValueError("Portfolio volatility is zero, cannot compute Sharpe Ratio. - Check your weights or return date.")

    sharpe_ratio = port_return / port_volatility
    return {'annual_return': port_return, 'annual_volatility': port_volatility, 'sharpe_ratio': sharpe_ratio}


def historical_var(returns, confidence_level=0.99):
    return -np.percentile(returns, (1 - confidence_level) * 100)

def parametric_var(returns, confidence_level=0.99):
    mu = returns.mean() # mean
    sigma = returns.std()  # standard deviation
    z_score = stats.norm.ppf(1 - confidence_level)
    return -(mu + z_score * sigma)

def cvar(returns, confidence_level=0.99):
    var = historical_var(returns, confidence_level)
    return -returns[returns < -var].mean()  # CVaR is the average of returns below the VaR threshold

def max_drawdown(returns):
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    return drawdown.min()  # Return the maximum drawdown (most negative value)