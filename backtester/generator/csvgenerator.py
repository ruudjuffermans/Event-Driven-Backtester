from .generator import Generator
import numpy as np
import pandas as pd
import os
from pathlib import Path

from ..events import MarketEvent


class CSVGenerator(Generator):
    def __init__(self, symbol_list):
        self.csv_dir = Path.cwd() / "data"
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
        self._load()

    def register(self, events):
        self.events = events

    def _load(self):
        combined_index = None
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = pd.io.parsers.read_csv(
                os.path.join(self.csv_dir, "%s.csv" % symbol),
                header=0,
                index_col=0,
                names=[
                    "datetime",
                    "open",
                    "high",
                    "low",
                    "close",
                    "adj_close",
                    "volume",
                ],
            )

            # Combine the index to pad forward values
            if combined_index is None:
                combined_index = self.symbol_data[symbol].index
            else:
                combined_index.union(self.symbol_data[symbol].index)

            # Set the latest symbol_data to None
            self.latest_symbol_data[symbol] = []

        # Reindex the dataframes
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = (
                self.symbol_data[symbol]
                .reindex(index=combined_index, method="pad")
                .iterrows()
            )

    def _get_new_bar(self, symbol):
        for bar in self.symbol_data[symbol]:
            yield bar

    def get_latest_bar(self, symbol):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1]

    def get_latest_bars(self, symbol, N=1):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-N:]

    def get_latest_bar_datetime(self, symbol):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1][0]

    def get_latest_bar_value(self, symbol, value_type):
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return getattr(bars_list[-1][1], value_type)

    def get_latest_bars_values(self, symbol, value_type, N=1):
        try:
            bars_list = self.get_latest_bars(symbol, N)
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return np.array([getattr(bar[1], value_type) for bar in bars_list])

    def update_bars(self):
        for symbol in self.symbol_list:
            try:
                bar = next(self._get_new_bar(symbol))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.events.put(MarketEvent())
