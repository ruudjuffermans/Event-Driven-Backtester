from Event import Event


class SignalEvent(Event):
    """
    Signal event generated from a particular strategy, if signal met strategy conditions

    Parameters:
    symbol - The symbol for current asset.
    datetime - A datetime at which the signal is generated.
    signal_type - The signal type ('LONG', 'SHORT', 'EXIT')
    strength - strength of the signal --> TODO: this should be given from a risk class when applying multiple strats
    """

    def __init__(self, symbol, datetime, signal_type, strength):
        self.type = "SIGNAL"
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength
