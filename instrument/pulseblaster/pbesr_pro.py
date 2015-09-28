"""
PulseBlasterESR-PRO Module

The PulseBlasterESR-PRO module, which contains the PulseBlasterESRPRO object.

Importable:
  - PulseBlasterESRPRO
"""

from instrument.pulseblaster.base import *
from ctypes import *

__all__ = ['PulseBlasterESRPRO']

class PulseBlasterESRPRO(PulseBlaster):
    """PulseBlasterESR-PRO class.

    Parameters:
      ...

    Instance Attributes:
      ...

    Class Attributes:
      ...
    """
    def _connect(self):
        if self.pb_select_board(self.device_num) != 0:
            raise InstrumentError('cannot select board {0} to connect: {1}'.format(
                    self.device_num, self.pb_get_error()))
        if self.pb_init() != 0:
            raise InstrumentError('cannot initialize board {0}: {1}'.format(
                    self.device_num, self.pb_get_error()))
        pb_core_clock(self.clock_freq)

    def _disconnect(self):
        if self.pb_select_board(self.device) != 0:
            raise InstrumentError('cannot select board {0} to disconnect: {1}'.format(
                    self.device_num, self.pb_get_error()))
        if self.pb_stop() != 0:
            raise InstrumentError('cannot stop board {0}: {1}'.format(
                    self.device_num, self.pb_get_error()))
        if self.pb_close() != 0:
            raise InstumentError('cannot close board {0}: {1}'.format(
                    self.device_num, self.pb_get_error()))

    def _reset(self):
        if self.pb_select_board(self.device) != 0:
            raise InstrumentError('cannot select board {0} to reset: {1}'.format(
                    self.device_num, self.pb_get_error()))
        if self.pb_reset() != 0:
            raise InstrumentError('cannot reset board {0}: {1}'.format(
                    self.device_num, self.pb_get_error()))

    # TODO(Jeffrey): Perhaps make nicer way to write instructions? Some are a
    # real pain to write.

