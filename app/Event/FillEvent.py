from Event import Event

class FillEvent(Event):
    """
    Fill event once an order based on the response from the broker

    Parameters:
    datetime - A datetime at which the signal is created.
    symbol - The symbol for current asset.
    exchange - The exchange, broker where the order is filled
    quantity - quantity filled
    direction
    fill_cost - can contain commission already
    commission - Defaulted to None if non specified
    """

    def __init__(self, datetime, symbol, exchange, quantity, direction, fill_cost, commission=None):

        self.type = "FILL"
        self.datetime = datetime
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        # Calculate commission
        if commission is None:
            self.commission = self._calculate_commission()
        else:
            self.commission = commission

    def _calculate_commission(self):
        """
        TODO: Commission fees to be implemented
        """
        # between 1 and 2%
        return max(1.5, 0.015 * self.quantity)
