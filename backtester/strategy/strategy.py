from abc import abstractmethod


class Strategy:
    @abstractmethod
    def calculate(self):
        raise NotImplementedError("Should implement calculate_signals()")
