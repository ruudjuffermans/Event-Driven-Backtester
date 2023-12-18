from Indicator import Indicator
from Event import MarketEvent

import numpy as np


class MAIndicator(Indicator):

    def __init__(self,  symbol, name, window_size, bars, events ):
        self.name = name
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.symbol = symbol
        self.events = events
        self.window_size = window_size
        self.data = dict()

    @classmethod
    def prepare(cls, symbol, name, window_size):
        def factory_method(**kwargs):
            return cls(symbol, name , window_size, **kwargs)
        return factory_method

    def calculate(self):
        """
        Generates a new set of signals based on the MAC
        SMA with the short window crossing the long window
        meaning a long entry and vice versa for a short entry.
        Parameters
        event - A MarketEvent object.
        """


        for symbol in self.symbol_list:
            bars = self.bars.get_latest_bars_values(symbol, "close", N=self.window_size)
            i = self.bars.get_latest_bar_datetime(symbol)

            if bars is not None and bars != []:
                ma=0
                if len(bars) >= self.window_size:
                    ma = np.mean( bars[-self.window_size:] )
                self.data[i]=ma 

