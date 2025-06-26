import numpy as np
import pandas as pd

def calculate_performance(portfolio: pd.Series, risk_free_rate: float = 0.0):
    """
    Calculate total return and Sharpe ratio for a portfolio value series.
    """
    returns = portfolio.pct_change().dropna()
    total_return = (portfolio.iloc[-1] / portfolio.iloc[0]) - 1
    sharpe_ratio = (returns.mean() - risk_free_rate/252) / (returns.std() + 1e-9) * np.sqrt(252)
    return {
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio
    } 