# import useful libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def rolling_var_backtest(portfolio_returns, weights=None, window=252, confidence_level=0.99):
    """
    Walk-forward backtest: Here, we estimate VaR on rolling window, checking if the next day's loss exceeds it.

    """

    violations = []
    var_series = []


    for i in range(window, len(portfolio_returns)):
        window_returns = portfolio_returns.iloc[i-window:i]
        var = -np.percentile(window_returns, (1-confidence_level)*100)
        actual_return = portfolio_returns.iloc[i]

        var_series.append(var)
        violations.append(1 if actual_return < -var else 0)

    violations = np.array(violations)
    var_series = np.array(var_series)
    actual_out_of_sample = portfolio_returns.iloc[window:].values

    return violations, var_series, actual_out_of_sample


def kupiec_test(violations, confidence_level=0.99, n_obs=None):
    """
    This tests whether the observed violation rate matches the expected rate (1 - confidence_level)
    """

    n = n_obs or len(violations)
    x = violations.sum()
    p = 1 - confidence_level
    p_hat = x / n

    if x == 0 or x == n:
        return {'violations': x, 'rate': p_hat, 'expected_rate': p, 'result': 'Cannot compute'}


    # Likelihood ratio statistics

    lr = -2 * (np.log((p**x) * ((1-p)**(n-x))) -
               np.log((p_hat**x) * ((1-p_hat)**(n-x))))
    
    p_value = 1 - stats.chi2.cdf(lr, df=1)
    
    return {
        'violations': int(x),
        'total_observations': n,
        'violation_rate': f"{p_hat:.2%}",
        'expected_rate': f"{p:.2%}",
        'LR_statistic': round(lr, 4),
        'p_value': round(p_value, 4),
        'result': 'PASS' if p_value > 0.05 else 'FAIL'}