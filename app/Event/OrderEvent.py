from Event import Event

class OrderEvent(Event):
    """
    Order event to be sent to a broker api. It takes into account the quantity,
    type of ordering, and direction (long, short, exit...)

    Parameters:
    symbol - The symbol for current asset.
    order_type - Whether is it a 'MARKET' or 'LIMIT' order
    quantity --> TODO: this should be implemented in a risk class (Kelly Criterion, etc)
    direction - 1 or -1 based on the type
    """

    def __init__(self, symbol, order_type, quantity, direction):
        self.type = "ORDER"
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        """
        Outputs the values within the Order.
        """
        print("Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s") % \
        (self.symbol, self.order_type, self.quantity, self.direction)
