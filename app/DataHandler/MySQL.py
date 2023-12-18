from DataHandler import DataHandler
from utils import mysql

from Event import MarketEvent


class MySQLDataHandler(DataHandler):
    """
    HistoricMySQLDataHandler is designed to read a MySQL database for each requested symbol from disk and 
    provide an interface to obtain the "latest" bar in a manner identical to a live trading interface.
    """

    def __init__(self, events, symbol_list, window):

        """
        Initialises the historic data handler by requesting
        the location of the database and a list of symbols.
        It will be assumed that all price data is in a table called 
        'symbols', where the field 'symbol' is a string in the list.
        Parameters:
        events - The Event Queue.
        db_host - host of the database
        db_user - database user
        db_pass - password to access database
        db_name - database's name
        symbol_list - A list of symbol stringss
        """

        self.events = events
        self.window = window
        self.symbol_list = symbol_list
        self.symbol_data = {}
        self.latest_symbol_data = {}

        self.continue_backtest = True
        self.db=mysql()


    def _load(self, symbol, columns):
        pass
        # db = MySQL()
        # print(db.get())



        # sql = SELECT {},{},{},{},{},{},{}
        #         FROM {}.format(columns[0],
        #                             columns[1],
        #                                 columns[2],
        #                                     columns[3],
        #                                       columns[4],
        #                                         columns[5],
        #                                             columns[6],
        #                                                 symbol)

        # return pd.read_sql_query(sql, con=connection, index_col="datetime")

    # def _data_conversion_from_database(self):
    #     """
    #     Opens the database files, converting them into 
    #     pandas DataFrames within a symbol dictionary.
    #     For this handler it will be assumed that the data is
    #     assumed to be stored in a database with similar columns 
    #     as the pandas dataframes. Thus, the format will be respected.
    #     """

    #     combined_index = None
    #     columns = ["datetime","open","high","low","close","volume","adj_close"]

    #     for symbol in self.symbol_list:
    #         self.symbol_data[symbol] = self._get_data_from_database(symbol, columns)


    #         # Combine the index to pad forward values
    #         if combined_index is None:
    #             combined_index = self.symbol_data[symbol].index
    #         else:
    #             combined_index.union(self.symbol_data[symbol].index)

    #         # Set the latest symbol_data to None
    #         self.latest_symbol_data[symbol] = []

    #     # Reindex the dataframes
    #     for symbol in self.symbol_list:
    #         self.symbol_data[symbol] = self.symbol_data[symbol].reindex(index=combined_index, method="pad").iterrows()

    # def _get_new_bar(self, symbol):
    #     """
    #     Returns the latest bar from the data feed as a tuple of 
    #     (symbol, datetime, open, low, high, close, volume, adj_close).
    #     """
    #     for bar in self.symbol_data[symbol]:
    #         yield bar


    # def get_latest_bar(self, symbol):
    #     """
    #     Returns the last bar from the latest_symbol list.
    #     """

    #     try:
    #         bars_list = self.latest_symbol_data[symbol]
    #     except KeyError:
    #         print("That symbol is not available in the historical data set.")
    #         raise
    #     else:
    #         return bars_list[-1]

    # def get_latest_bars(self, symbol, N=1):
    #     """
    #     Returns the last N bars from the latest_symbol list,
    #     or N-k if less available.
    #     """

    #     try:
    #         bars_list = self.latest_symbol_data[symbol]
    #     except KeyError:
    #         print("That symbol is not available in the historical data set.")
    #         raise
    #     else:
    #         return bars_list[-N:]

    # def get_latest_bar_datetime(self, symbol):
    #     """
    #     Returns a Python datetime object for the last bar.
    #     """
    #     try:
    #         bars_list = self.latest_symbol_data[symbol]
    #     except KeyError:
    #         print("That symbol is not available in the historical data set.")
    #         raise
    #     else:
    #         return bars_list[-1][0]

    # def get_latest_bar_value(self, symbol, value_type):
    #     """
    #     Returns one of the Open, High, Low, Close, Volume or OI
    #     values from the pandas Bar series object.
    #     """
    #     try:
    #         bars_list = self.latest_symbol_data[symbol]
    #     except KeyError:
    #             print("That symbol is not available in the historical data set.")
    #             raise
    #     else:
    #         return getattr(bars_list[-1][1], value_type)


    # def get_latest_bars_values(self, symbol, value_type, N=1):
    #     """
    #     Returns the last N bar values from the
    #     latest_symbol list, or N-k if less available.
    #     """
    #     try:
    #         bars_list = self.get_latest_bars(symbol, N) # bars_list = bars_list[-N:]
    #     except KeyError:
    #         print("That symbol is not available in the historical data set.")
    #         raise
    #     else:
    #         return np.array([getattr(bar[1], value_type) for bar in bars_list])

    # def update_bars(self):
    #     """
    #     Pushes the latest bar to the latest_symbol_data structure
    #     for all symbols in the symbol list.
    #     """
    #     for symbol in self.symbol_list:
    #         try:
    #             bar = next(self._get_new_bar(symbol))
    #         except StopIteration:
    #             self.continue_backtest = False
    #         else:
    #             if bar is not None:
    #                 self.latest_symbol_data[symbol].append(bar)
    #     self.events.put(MarketEvent())
