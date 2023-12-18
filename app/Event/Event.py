import datetime

import queue

from abc import ABCMeta, abstractmethod

class Event(metaclass=ABCMeta):
    """
    Event is base class providing an interface for all subsequent 
    (inherited) events, that will trigger further events in the 
    trading infrastructure.   
    """
    pass