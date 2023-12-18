from DataHandler import CSVDataHandler, YahooDataHandler, BinanceDataHandler
from datetime import datetime
from pathlib import Path

# Import the different components of the backtester
from Backtest import Backtest
from Execution import SimulatedExecutionHandler
from Portfolio import Portfolio
from Window import Window
#The different strategies that can be used in the backtester
# from Strategies.Buy_and_hold_strat import BuyAndHoldStrat
from Strategy import MACrossOverStrategy, ETFForecastStrategy
from Indicator import MAIndicator


print("running")



if __name__ == "__main__":
    data_dir = Path.cwd() / 'data'  # For reading from CSV files
    symbol_list = ['BTCUSDT']
    initial_capital = 100000.0
    start_date = datetime(2022, 1, 1, 0, 0, 0)
    end_date = datetime(2023, 1, 1, 0, 0, 0)
    interval = '1m'
    heartbeat = 0.0

    backtest = Backtest(data_dir,  # data directory of CSV files
                        symbol_list,  # list of symbols
                        [MAIndicator.prepare(window_size=20, name="SMALL",symbol="BTCUSDT"),MAIndicator.prepare(window_size=40, name="BIG", symbol="BTCUSDT")],
                        initial_capital,  # initial capital available for trading
                        heartbeat,  # heartbeat to count time in real live trading simulation
                        Window(start=start_date, end=end_date, interval=interval),
                        BinanceDataHandler,  # data management method
                        SimulatedExecutionHandler,  # Type of execution in relationship to broker
                        Portfolio,  # portfolio management method
                        MACrossOverStrategy)  # strategy chosen
    
    backtest.simulate_trading()