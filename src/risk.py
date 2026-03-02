import pandas as pd
import numpy as np

log_returns = pd.read_csv('../data/log_returns.csv', index_col=0, parse_dates=True)
weights = np.array([0.30, 0.25, 0.20, 0.15, 0.10])

portfolio_returns = log_returns.dot(weights)