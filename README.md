# Event-Driven Backtester

## Overview
The `event-driven-backtester` is a Python-based backtesting framework designed for quantitative trading strategies. It simulates the execution of trading strategies on historical data, allowing traders and researchers to evaluate the performance of their strategies before applying them in live trading environments. The system follows an event-driven architecture, making it extensible and suitable for a wide range of financial markets.

## Features
- Event-Driven Architecture: Reacts to market data updates, signals, order events, and fills.
- Strategy Integration: Easily plug in custom trading strategies.
- Historical Data Support: Test strategies on historical data through a CSV file interface.
- Portfolio Management: Simulates portfolio management and tracking of positions.
- Order Execution Simulation: Simulates order execution, including handling of transactions and potential slippage.

## Installation
To get started with event-driven-backtester, clone this repository and install the required dependencies:
```bash
git https://github.com/ruudjuffermans/Event-Driven-Backtester.git
cd Event-Driven-Backtester
pip install -r requirements.txt
```

## Usage
To run a backtest:
1. Define your trading strategy by subclassing MACrossOverStrategy.
2. Prepare your historical data in CSV format.
3. Set up the backtesting environment by specifying the initial portfolio balance, symbols to trade, and historical data window.
4. Start the backtest loop `python ./example.py`.

Here is the content of the example file:
```python
from datetime import datetime

from backtester.loop import Loop
from backtester.generator import CSVGenerator
from backtester.execution import SimulatedExecutionHandler
from backtester.portfolio import Portfolio
from backtester.strategy import MACrossOverStrategy

from backtester.types import Window

symbol_list = ["BIG"]
window = Window(
    start=datetime(2016, 1, 1, 0, 0, 0),
    end=datetime(2021, 1, 1, 0, 0, 0),
    interval="1d",
)

generator = CSVGenerator(symbol_list)
portfolio = Portfolio(window, 100000.0)
strategy = MACrossOverStrategy()
execution = SimulatedExecutionHandler()

backtest = Loop(generator, execution, portfolio, strategy, 0.0)

backtest.start()
```