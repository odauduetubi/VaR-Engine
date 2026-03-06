import  numpy as np
from scipy.optimize import minimize

def efficient_frontier(log_returns, n_portfolios=5000, risk_free=0.05):
    n = log_returns.shape[1]
    mean_returns = log_returns.mean() * 252
    cov_matrix = log_returns.cov() * 252

    results = {'returns': [], 'volatility': [], 'sharpe': [], 'weights': []}

    for _ in range(n_portfolios):
        w = np.random.dirichlet(np.ones(n))  # Random weights summing to 1
        ret = np.dot(w, mean_returns)
        vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
        sharpe = (ret - risk_free) / vol

        results['returns'].append(ret)
        results['volatility'].append(vol)
        results['sharpe'].append(sharpe)
        results['weights'].append(w)

    return results


def max_sharpe_portfolio(log_returns, risk_free=0.05):
    n = log_returns.shape[1]
    mean_returns = log_returns.mean() * 252
    cov_matrix = log_returns.cov() * 252

    def neg_sharpe(w):
        ret = np.dot(w, mean_returns)
        vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
        return -(ret - risk_free) / vol
    
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
    bounds = tuple((0, 1) for _ in range(n))
    w0 = np.ones(n) / n

    result = minimize(neg_sharpe, w0, bounds=bounds, constraints=constraints)
    return result.x
