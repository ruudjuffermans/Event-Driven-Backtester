from DataHandler import CSVDataHandler
from datetime import datetime
from pathlib import Path

# Import the different components of the backtester
from Backtest import Backtest
from Execution import SimulatedExecutionHandler
from Portfolio import Portfolio
from Window import Window

# The different strategies that can be used in the backtester
# from Strategies.Buy_and_hold_strat import BuyAndHoldStrat
from Strategy import MACrossOverStrategy
from Indicator import MAIndicator


print("running")


if __name__ == "__main__":
    data_dir = Path.cwd() / "data"
    symbol_list = ["AAPL"]
    initial_capital = 100000.0
    start_date = datetime(2022, 1, 1, 0, 0, 0)
    end_date = datetime(2023, 1, 1, 0, 0, 0)
    interval = "1m"
    heartbeat = 0.0

    backtest = Backtest(
        data_dir,
        symbol_list,
        [
            MAIndicator.prepare(window_size=20, name="SMALL", symbol="AAPL"),
            MAIndicator.prepare(window_size=40, name="BIG", symbol="AAPL"),
        ],
        initial_capital,
        heartbeat,
        Window(start=start_date, end=end_date, interval=interval),
        CSVDataHandler,
        SimulatedExecutionHandler,
        Portfolio,
        MACrossOverStrategy,
    )

    backtest.simulate_trading()
