"""
Power Supply Module
The power supply module, which contains the power supply
Importable:
  - PowerSupply
"""

"""So this provides some common commands?"""
from instrument import *

__all__ = ['PowerSupply']

class PowerSupply(Instrument):
    def get_power(self):
        raise NotImplemented()

    def set_power(self, power):
        raise NotImplemented()

    def get_current(self):
        raise NotImplemented()

    def set_current(self, current):
        raise NotImplemented()