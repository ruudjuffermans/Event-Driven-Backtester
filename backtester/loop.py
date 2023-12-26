import pprint

import queue
import time

from .events import MarketEvent, SignalEvent, OrderEvent, FillEvent
from .generator import CSVGenerator


class Loop:
    def __init__(
        self,
        data_handler,
        execution_handler,
        portfolio,
        strategy,
        heartbeat,
    ):
        self.heartbeat = heartbeat

        self.data_handler = data_handler
        self.execution_handler = execution_handler
        self.portfolio = portfolio
        self.strategy = strategy

        self.events = queue.Queue()
        self.signals = 0
        self.orders = 0
        self.fills = 0
        self.num_strats = 1

        self._set_datahandler()
        self._set_portfolio()
        self._set_execution_handler()
        self._set_strategy()

    def _set_datahandler(self):
        if isinstance(self.data_handler, CSVGenerator):
            self.data_handler.register(self.events)
        else:
            raise NotImplementedError("Data feed not implemented")

    def _set_strategy(self):
        self.strategy.register(self.data_handler, self.events)

    def _set_portfolio(self):
        self.portfolio.register(self.data_handler, self.events)

    def _set_execution_handler(self):
        self.execution_handler.register(self.events)

    def _run_backtest(self):
        """
        Executes the backtest.
        """
        while True:
            if self.data_handler.continue_backtest:
                self.data_handler.update_bars()
            else:
                break
            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if isinstance(event, MarketEvent):
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

    def start(self):
        """
        Simulates the backtest and outputs portfolio performance.
        """
        self._run_backtest()
        self._output_performance()
