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
