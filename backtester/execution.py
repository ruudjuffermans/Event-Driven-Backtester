from abc import abstractmethod
from datetime import datetime

from .events import FillEvent, OrderEvent


class ExecutionHandler:
    def register(self, events):
        self.events = events

    @abstractmethod
    def execute_order(self, event):
        raise NotImplementedError("Should implement execute_order()")


class SimulatedExecutionHandler(ExecutionHandler):
    def __init__(self):
        pass

    def execute_order(self, event):
        if isinstance(event, OrderEvent):
            fill_event = FillEvent(
                datetime.utcnow(),
                event.symbol,
                "BT",
                event.quantity,
                event.direction,
                None,
            )
            self.events.put(fill_event)
