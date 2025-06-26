import numpy as np
import pandas as pd

def mean_reversion(data: pd.DataFrame, window: int = 20, threshold: float = 0.02) -> pd.DataFrame:
    """
    Mean reversion strategy: Buy when price is below MA by threshold, sell when above.
    Adds 'MA', 'Signal', and 'Position' columns.
    """
    data = data.copy()
    data['MA'] = data['Close'].rolling(window=window).mean()
    data['Signal'] = 0
    data.loc[data['Close'] < (1 - threshold) * data['MA'], 'Signal'] = 1  # Buy
    data.loc[data['Close'] > (1 + threshold) * data['MA'], 'Signal'] = -1 # Sell
    data['Position'] = data['Signal'].diff()
    return data 