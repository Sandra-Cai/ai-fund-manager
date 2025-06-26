import numpy as np
import pandas as pd

def sma_crossover(data: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> pd.DataFrame:
    """
    Adds SMA crossover signals to the DataFrame.
    Returns the DataFrame with 'SMA_Short', 'SMA_Long', 'Signal', and 'Position' columns.
    """
    data = data.copy()
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    data['Signal'] = 0
    data.loc[short_window:, 'Signal'] = np.where(
        data['SMA_Short'][short_window:] > data['SMA_Long'][short_window:], 1, 0)
    data['Position'] = data['Signal'].diff()
    return data 