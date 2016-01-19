"""
Sensor Module
The Sensor module, which contains the Sensor
Importable:
  - Sensor
"""

"""So this provides some common commands?"""
from instrument import *

__all__ = ['Sensor']

class Sensor(Instrument):
    def get_power(self):
        raise NotImplemented()

    def set_power(self, power):
        raise NotImplemented()

    def get_current(self):
        raise NotImplemented()

    def set_current(self, current):
        raise NotImplemented()