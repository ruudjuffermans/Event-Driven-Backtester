import pprint

import queue
import time

from Event import MarketEvent, SignalEvent, OrderEvent, FillEvent
from Window import Window


class Backtest():
    def __init__(self, data_dir, symbol_list, indicator_list, initial_capital,
                 heartbeat, window,
                 data_handler, execution_handler, portfolio, strategy
                 ):
        self.symbol_list = symbol_list
        self.indicator_list = indicator_list
        self.window = window
        self.data_dir = data_dir
        self.initial_capital = initial_capital
        self.heartbeat = heartbeat

        self.data_handler_cls = data_handler
        self.execution_handler_cls = execution_handler
        self.portfolio_cls = portfolio
        self.strategy_cls = strategy

        self.events = queue.Queue()
        self.signals = 0
        self.orders = 0
        self.fills = 0
        self.num_strats = 1

        self._set_datahandler()
        self._set_indicators()
        self._set_portfolio()
        self._set_execution_handler()
        self._set_strategy()


    def _set_datahandler(self):
        """
        Generates the trading instance objects from
        their class types.
        """
            
        print("Creating DataHandler, Strategy, Portfolio and ExecutionHandler")
        if self.data_handler_cls.__name__ == 'CSVDataHandler':
            self.data_handler = self.data_handler_cls(self.events, self.symbol_list)

        # TODO --> Implement a better selection mode
        elif self.data_handler_cls.__name__ == 'YahooDataHandler':
            self.data_handler = self.data_handler_cls(self.events, self.symbol_list, self.window)
        elif self.data_handler_cls.__name__ == 'BinanceDataHandler':
            self.data_handler = self.data_handler_cls(self.events, self.symbol_list, self.window)
        else:
            raise NotImplementedError("Data feed not implemented")
        
    def _set_indicators(self):
        self.indicators=[]
        for indicator in self.indicator_list:
            self.indicators.append(indicator(bars=self.data_handler, events=self.events))
            
    def _set_strategy(self):
        self.strategy = self.strategy_cls(self.data_handler, self.indicators, self.events)

    def _set_portfolio(self):
        self.portfolio = self.portfolio_cls(self.data_handler, self.events, self.window, self.initial_capital)

    def _set_execution_handler(self):
        self.execution_handler = self.execution_handler_cls(self.events)

    def _run_backtest(self):
        """
        Executes the backtest.
        """
        e = 0
        i = 0
        while True:
            i += 1
            print("i", i)
            # Update the market bars
            if self.data_handler.continue_backtest == True:
                self.data_handler.update_bars()
            else:
                break

            # Handle the events
            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        e += 1
                        print("e",e)
                        if isinstance(event, MarketEvent):
                            for indicator in self.indicators:
                                indicator.calculate()
                            self.strategy.calculate(event)
                            self.portfolio.update_timeindex(event)

                        elif isinstance(event, SignalEvent):
                            self.signals += 1
                            self.portfolio.update_signal(event)

                        elif isinstance(event, OrderEvent):
                            self.orders += 1
                            self.execution_handler.execute_order(event)

                        elif isinstance(event, FillEvent):
                            self.fills += 1
                            self.portfolio.update_fill(event)

            time.sleep(self.heartbeat)

    def _output_performance(self):
        """
        Outputs the strategy performance from the backtest.
        """
        self.portfolio.create_equity_curve_dataframe()

        print("Creating summary stats...")
        stats = self.portfolio.output_summary_stats()

        print("Creating equity curve...")
        print(self.portfolio.equity_curve.tail(10))

        pprint.pprint(stats)
        print("Signals: %s" % self.signals)
        print("Orders: %s" % self.orders)
        print("Fills: %s" % self.fills)
    
    def simulate_trading(self):
        """
        Simulates the backtest and outputs portfolio performance.
        """
        self._run_backtest()
        self._output_performance()