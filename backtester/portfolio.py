import pandas as pd
from .events import FillEvent, OrderEvent, SignalEvent
from .performance import create_sharpe_ratio, create_drawdowns
from math import floor


class Portfolio:
    def __init__(self, window, initial_capital=100000.0):
        self.start_date = window.start
        self.initial_capital = initial_capital

    def register(self, bars, events):
        self.bars = bars

        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.current_positions = {symbol: 0 for symbol in self.symbol_list}
        self.all_positions = self.define_all_positions()
        self.all_holdings = self.define_all_holdings()
        self.current_holdings = self.define_current_holdings()

    def define_all_positions(self):
        positions = {symbol: 0 for symbol in self.symbol_list}
        positions["datetime"] = self.start_date
        return [positions]

    def define_all_holdings(self):
        holdings = {symbol: 0.0 for symbol in self.symbol_list}
        holdings["datetime"] = self.start_date
        holdings["cash"] = self.initial_capital
        holdings["commission"] = 0.0
        holdings["total"] = self.initial_capital
        return [holdings]

    def define_current_holdings(self):
        holdings = {symbol: 0.0 for symbol in self.symbol_list}
        holdings["cash"] = self.initial_capital
        holdings["commission"] = 0.0
        holdings["total"] = self.initial_capital
        return holdings

    def update_timeindex(self, event):
        latest_datetime = self.bars.get_latest_bar_datetime(self.symbol_list[0])

        positions = {
            symbol: self.current_positions[symbol] for symbol in self.symbol_list
        }
        positions["datetime"] = latest_datetime

        self.all_positions.append(positions)
        holdings = {symbol: 0.0 for symbol in self.symbol_list}
        holdings["datetime"] = latest_datetime
        holdings["cash"] = self.current_holdings["cash"]
        holdings["commission"] = self.current_holdings["commission"]
        holdings["total"] = self.current_holdings["cash"]

        for symbol in self.symbol_list:
            market_value = self.current_positions[
                symbol
            ] * self.bars.get_latest_bar_value(symbol, "close")
            holdings[symbol] = market_value
            holdings["total"] += market_value

        self.all_holdings.append(holdings)

    def update_positions_after_fill(self, fill):
        fill_dir = 0
        if fill.direction == "BUY":
            fill_dir = 1
        if fill.direction == "SELL":
            fill_dir = -1
        self.current_positions[fill.symbol] += fill_dir * fill.quantity

    def update_holdings_after_fill(self, fill):
        fill_dir = 0
        if fill.direction == "BUY":
            fill_dir = 1
        if fill.direction == "SELL":
            fill_dir = -1
        fill_cost = self.bars.get_latest_bar_value(fill.symbol, "close")
        cost = fill_dir * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings["commission"] += fill.commission
        self.current_holdings["cash"] -= cost + fill.commission
        self.current_holdings["total"] -= cost + fill.commission

    def update_fill(self, event):
        if isinstance(event, FillEvent):
            self.update_positions_after_fill(event)
            self.update_holdings_after_fill(event)

    def generate_naive_order(self, signal):
        order = None
        symbol = signal.symbol
        direction = signal.signal_type
        strength = signal.strength

        mkt_quantity = floor(100 * strength)
        current_quantity = self.current_positions[symbol]
        order_type = "MKT"

        if direction == "LONG" and current_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, "BUY")
        if direction == "SHORT" and current_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, "SELL")
        if direction == "EXIT" and current_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(current_quantity), "SELL")
        if direction == "EXIT" and current_quantity < 0:
            order = OrderEvent(symbol, order_type, abs(current_quantity), "BUY")
        return order

    def update_signal(self, event):
        if isinstance(event, SignalEvent):
            order_event = self.generate_naive_order(event)
            self.events.put(order_event)

    def create_equity_curve_dataframe(self):
        equity_curve = pd.DataFrame(self.all_holdings)
        equity_curve.set_index("datetime", inplace=True)
        equity_curve["returns"] = equity_curve["total"].pct_change()
        equity_curve["equity_curve"] = (1.0 + equity_curve["returns"]).cumprod()
        self.equity_curve = equity_curve

    def output_summary_stats(self):
        total_return = self.equity_curve["equity_curve"][-1]
        returns = self.equity_curve["returns"]
        pnl = self.equity_curve["equity_curve"]
        sharpe_ratio = create_sharpe_ratio(returns, periods=252 * 60 * 6.5)
        drawdown, max_dd, max_dd_duration = create_drawdowns(pnl)
        self.equity_curve["drawdown"] = drawdown

        stats = [
            ("Total Return", "%0.2f%%" % ((total_return - 1.0) * 100.0)),
            ("Sharpe Ratio", "%0.2f" % sharpe_ratio),
            ("Max Drawdown", "%0.2f%%" % (max_dd * 100.0)),
            ("Max Drawdown Duration", "%d" % max_dd_duration),
        ]
        self.equity_curve.to_csv("equity.csv")
        return stats
