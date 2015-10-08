"""
VisaInstrument Module

VisaInstrument module, which contains

Importable:
  - VisaInstrument
"""

import visa
from instrument import *

__all__ = ['VisaInstrument']

class VisaInstrument(Instrument):
    """Visa Instrument Interface.

    The Visa Instrument interface, which needs a better docstring.

    Parameters:
      - address (str):
      ...

    Instance Attributes:
      - address (str):
      - _instr (visa.resource.Resource):
      ...

    Class Attributes:
      ...
    """
    def __init__(self, address, **kwargs):
        Instrument.__init__(self, **kwargs)
        self.address = address

    def _connect(self):
        self._instr = visa.ResourceManager().open_resource(self.address)

    def _disconnect(self):
        self._instr.close()
        self._instr = None

    def _read(self, string):
        try:
            return self._instr.query(string)
        except visa.VisaIOError as e:
            raise InstrumentError('Error reading command ({0}): {1}'.format(
                    string, e.message))
        except TypeError:
            raise InstrumentError('{0} instrument is not connected.'.format(
                    type(self).__name__)

    def _write(self, string):
        try:
            self._instr.write(string)
        except visa.VisaIOError as e:
            raise InstrumentError('Error reading command ({0}): {1}'.format(string, e.message))
        except TypeError:
            raise InstrumentError('{0} instrument is not connected.'.format(
                    type(self).__name__)
    
    
    ######################
    ## Abstract Methods ##
    ######################

    def check_error(self):
        """Checks instrument for an error. If an error was encountered, then
        this function raises an InstrumentError.
        
        Always called after a read or write operation.
        """
        return NotImplemented

