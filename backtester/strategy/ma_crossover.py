from .strategy import Strategy
from ..events import MarketEvent


class MACrossOverStrategy(Strategy):
    def __init__(self, short_window=100, long_window=400):
        self.short_window = short_window
        self.long_window = long_window

    def register(self, bars, events):
        self.bars = bars
        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        bought = {symbol: "OUT" for symbol in self.symbol_list}
        return bought

    def calculate(self, event):
        if isinstance(event, MarketEvent):
            for symbol in self.symbol_list:
                bars = self.bars.get_latest_bars_values(
                    symbol, "close", N=self.long_window
                )
                bar_datetime = self.bars.get_latest_bar_datetime(symbol)

                if bars is not None and bars != []:
                    print(bar_datetime)

                    # long_sma = np.mean( bars[-self.long_window:] )

                    # dt = datetime.datetime.utcnow()
                    # signal_type = ""
                    # strength = 1.0

                    # if short_sma > long_sma and self.bought[symbol] == "OUT":
                    #     print("LONG position at: %s" % bar_datetime)
                    #     signal_type = "LONG"
                    #     signal = SignalEvent(symbol, dt, signal_type, strength)
                    #     self.events.put(signal)
                    #     self.bought[symbol] = "LONG"

                    # elif short_sma < long_sma and self.bought[symbol] == "LONG":
                    #     print("SHORT position at: %s" % bar_datetime)
                    #     signal_type = "EXIT"
                    #     signal = SignalEvent(symbol, dt, signal_type, strength)
                    #     self.events.put(signal)
                    #     self.bought[symbol] = "OUT"
