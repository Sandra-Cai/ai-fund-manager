import pandas as pd
import numpy as np
from fastapi import FastAPI, Query
import yfinance as yf
import uvicorn

from strategies import sma_crossover, mean_reversion, momentum_strategy
from utils.performance import calculate_performance

# --- Data Loading and Preprocessing ---
def load_data(symbol: str, period: str = '1y'):
    data = yf.download(symbol, period=period)
    data = data.dropna()
    return data

# --- Strategy Selector ---
STRATEGIES = {
    'sma_crossover': sma_crossover,
    'mean_reversion': mean_reversion,
    'momentum': momentum_strategy
}

def apply_strategy(data, strategy_name: str):
    if strategy_name not in STRATEGIES:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    return STRATEGIES[strategy_name](data)

# --- Simple Backtest ---
def backtest(data):
    initial_capital = 10000
    positions = initial_capital * (data['Signal'].replace(-1, 0))
    returns = data['Close'].pct_change().fillna(0)
    portfolio = (positions.shift(1) * returns).cumsum() + initial_capital
    return portfolio

# --- FastAPI Endpoint ---
app = FastAPI()

@app.get("/backtest/{symbol}")
def run_backtest(symbol: str, strategy: str = Query('sma_crossover', enum=list(STRATEGIES.keys()))):
    data = load_data(symbol)
    data = apply_strategy(data, strategy)
    portfolio = backtest(data)
    perf = calculate_performance(portfolio)
    return {
        "symbol": symbol,
        "strategy": strategy,
        "final_portfolio_value": float(portfolio.iloc[-1]),
        "total_return": perf['total_return'],
        "sharpe_ratio": perf['sharpe_ratio'],
        "history": portfolio.tail(30).round(2).to_dict()
    }

if __name__ == "__main__":
    # Example usage in script mode
    symbol = "AAPL"
    strategy = "sma_crossover"  # Change to 'mean_reversion' or 'momentum' to test others
    data = load_data(symbol)
    data = apply_strategy(data, strategy)
    portfolio = backtest(data)
    perf = calculate_performance(portfolio)
    print(f"Backtest for {symbol} using {strategy}")
    print(f"Final Portfolio Value: ${portfolio.iloc[-1]:.2f}")
    print(f"Total Return: {perf['total_return']*100:.2f}%")
    print(f"Sharpe Ratio: {perf['sharpe_ratio']:.2f}")
    # To run the API, uncomment the next line:
    # uvicorn.run(app, host="0.0.0.0", port=8000)
