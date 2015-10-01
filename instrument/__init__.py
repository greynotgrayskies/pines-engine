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
      - engine (Engine): The experiment engine.

    Instance Attributes:
      - _engine (Engine): The experiment engine.
    """

    def __init__(self, engine):
        self._engine = engine

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
        instrument to its default state. Will always be called upon the
        beginning of an experiment, and before disconnecting from an
        experiment.
        """
        return NotImplemented()

class InstrumentError(Exception):
    """Base exception raised by instruments."""
    pass

