"""
Instrument Module

Contains Instrument interface, which all instruments should inherit from.

Importable:
  - Instrument
  - InstrumentError
"""

__all__ = ['Instrument', 'InstrumentError']

class Instrument(object):
    """Instrument interface.

    The Instrument object interface, which all instrument definitions should
    inherit from. All instruments should have an attributed engine, methods to
    connect to and disconnect from an instrument, as well as a method to reset
    an instrument.

    Parameters:

    Instance Attributes:
      - _id (int): Instrument ID, for identification.

    Class Attributes:
      - num_instruments (int): Number of instruments instantiated.
    """
    num_instruments = 0

    def __init__(self):
        self._id = Instrument.num_instruments
        Instrument.num_instruments += 1

    def _connect(self):
        """Connect to an instrument. This function will always be called once
        upon engine initialization.
        """
        return NotImplemented()

    def _disconnect(self):
        """Terminate a connection to an instrument. Will always be called once
        upon engine tear down.
        """
        return NotImplemented()

    def _reset(self):
        """Resets an instrument. Performs a sequence of actions that resets an
        instrument to its default state. Will always be called once upon engine
        initialization and engine teardown. May also be called in between
        experiments, if desired.
        """
        return NotImplemented()

    def __str__(self):
        return '{0}(id:{1})'.format(type(self).__name__, self._id)

class InstrumentError(Exception):
    """Base exception raised by instruments."""
    pass

