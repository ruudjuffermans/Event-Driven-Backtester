from DataHandler import DataHandler
import yfinance as yf
import numpy as np

from Event import MarketEvent


class YahooDataHandler(DataHandler):
    """
    Get data directly from Yahoo Finance website, and provide an interface
    to obtain the "latest" bar in a manner identical to a live
    trading interface.
    """

    def __init__(self, events, symbol_list, window):
        """
        Initialize Queries from yahoo finance api to
        receive historical data transformed to dataframe

        Parameters:
        events - The Event Queue.
        symbol_list - A list of symbol strings.
        interval - 1d, 1wk, 1mo - daily, weekly monthly data
        start_date - starting date for the historical data (format: datetime)
        end_date - final date of the data (format: datetime)

        """

        self.events = events
        self.symbol_list = symbol_list
        self.window = window
        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
        self._load_data_from_Yahoo_finance()

    def _load_data_from_Yahoo_finance(self):
        """
        Queries yfinance api to receive historical data in csv file format
        """

        combined_index = None
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = yf.download(
                tickers=[symbol],
                start=self.window.start,
                end=self.window.end,
                interval=self.window.interval,
            )

            # rename columns for consistency
            self.symbol_data[symbol].rename(
                columns={
                    "Open": "open",
                    "High": "high",
                    "Low": "low",
                    "Close": "close",
                    "Adj Close": "adj_close",
                    "Volume": "volume",
                },
                inplace=True,
            )
            print(self.symbol_data[symbol])
            # rename index as well from 'Date' to 'datetime'
            self.symbol_data[symbol].index.name = "datetime"

            # create returns column (used for some strategies)
            self.symbol_data[symbol]["returns"] = (
                self.symbol_data[symbol]["adj_close"].pct_change() * 100.0
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
        """
        Returns the latest bar from the data feed as a tuple of
        (symbol, datetime, open, low, high, close, volume, adj_close, etc).
        """
        for bar in self.symbol_data[symbol]:
            yield bar

    def get_latest_bar(self, symbol):
        """
        Returns the last bar from the latest_symbol list.
        """

        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1]

    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """

        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-N:]

    def get_latest_bar_datetime(self, symbol):
        """
        Returns a Python datetime object for the last bar.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return bars_list[-1][0]

    def get_latest_bar_value(self, symbol, value_type):
        """
        Returns one of the Open, High, Low, Close, Volume or OI
        values from the pandas Bar series object.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return getattr(bars_list[-1][1], value_type)

    def get_latest_bars_values(self, symbol, value_type, N=1):
        """
        Returns the last N bar values from the
        latest_symbol list, or N-k if less available.
        """
        try:
            bars_list = self.get_latest_bars(symbol, N)
        except KeyError:
            print("That symbol is not available in the historical data set.")
            raise
        else:
            return np.array([getattr(bar[1], value_type) for bar in bars_list])

    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol in self.symbol_list:
            try:
                bar = next(self._get_new_bar(symbol))
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[symbol].append(bar)
        self.events.put(MarketEvent())
