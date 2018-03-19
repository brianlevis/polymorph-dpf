# Created by Brian Levis on 3/17/18

from .utils import *
from abc import ABC, abstractmethod

class Simulator(ABC):

    def set_price_floor(self, input_features, output_features):
        return 0.1 / 1000

