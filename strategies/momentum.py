import numpy as np
import pandas as pd

def momentum_strategy(data: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """
    Momentum strategy: Buy if return over lookback is positive, sell if negative.
    Adds 'Momentum', 'Signal', and 'Position' columns.
    """
    data = data.copy()
    data['Momentum'] = data['Close'].pct_change(periods=lookback)
    data['Signal'] = 0
    data.loc[data['Momentum'] > 0, 'Signal'] = 1
    data.loc[data['Momentum'] < 0, 'Signal'] = -1
    data['Position'] = data['Signal'].diff()
    return data 