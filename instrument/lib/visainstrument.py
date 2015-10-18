"""
VisaInstrument Module

VisaInstrument module, which contains the VisaInstrument interface, which is
used to communicate with instruments than can be connected to using the PyVISA
library.

Documentation for the PyVISA library can be found here:
https://pyvisa.readthedocs.org/en/stable/

Importable:
  - VisaInstrument
"""

import visa
from instrument import *

from functools import wraps

__all__ = ['VisaInstrument']

class VisaInstrument(Instrument):
    """Visa Instrument Interface.

    The Visa Instrument interface, which handles communication with instruments
    that can be connected to with with the PyVISA library. 

    The PyVISA library can handle connecting to and disconnecting from an
    instrument, as well as reading and writing to instruments. However, while
    instructions can be sent, instruments don't have a way of throwing errors,
    so instructions to check the error status code and error status message are
    required. The `check_error` decorator is used to denote functions that
    might write instructions that would cause an error in the instrument.

    Parameters:
      - address (str):
      ...

    Instance Attributes:
      - address (str):
      - _instr (visa.resource.Resource):
      ...

    Class Attributes:
      - _visamodule (module): Visa module used for communicating with
        instuments. Defined to facilitate testing. Do not modify otherwise.
      ...
    """
    _visamodule = visa

    def __init__(self, address, **kwargs):
        Instrument.__init__(self, **kwargs)
        self.address = address
        self._instr = None

    #######################
    ## Overriden Methods ##
    #######################

    def _connect(self):
        rm = VisaInstrument._visamodule.ResourceManager()
        # What error does this raise for an invalid address?
        self._instr = rm.open_resource(self.address)

    def _disconnect(self):
        self._instr.close()
        self._instr = None

    
    ############################
    ## VisaInstrument Methods ##
    ############################

    # TODO(Jeffrey): Some instructions need a delay before another instruction
    # can be sent to it. Perhaps add some sort of timed lock?
    def _read(self, instruction):
        """Sends a read instruction to a VISA instrument, and returns the
        resulting output.

        Parameters:
          - instruction (str): instruction sequence sent to the instrument.

        Output:
          - str: Resulting output from instruction.
        """
        if self._instr is None:
            raise InstrumentError('{0} is not connected.'.format(
                    self))
        try:
            return str(self._instr.query(instruction))
        except VisaInstrument._visamodule.VisaIOError as e:
            raise InstrumentError('Error reading {0} instruction ({1}): {2}'.format(
                    self, instruction, e.message))

    def _write(self, instruction):
        """Writes a instruction to an instrument.

        Parameters:
          - instruction (str): instruction sequence sent to the instrument.
        """
        if self._instr is None:
            raise InstrumentError('{0} is not connected.'.format(
                    self))
        try:
            self._instr.write(instruction)
        except VisaInstrument._visamodule.VisaIOError as e:
            raise InstrumentError('Error writing {0} instruction ({1}): {2}'.format(
                self, instruction, e.message))

    @staticmethod
    def check_error(fn):
        """A function decorator that is used to indicate that the error status
        of an instrument should be checked after a function is called.

        Only use to decorate instance methods. Class and static methods are
        probably incompatible.
        """
        @wraps(fn)
        def checked_fn(self, *args):
            val = fn(self, *args)
            err_no = self._get_error_no()
            if err_no != 0:
                # Most instruments clear the error message after checking even
                # just the error number, so the instruction is resent to
                # reprocure it.
                fn(self, *args)
                raise InstrumentError(NONZERO_ERROR_NO.format(
                        cls_name = type(self).__name__,
                        fn_name = fn.__name,
                        fn_args = ', '.join(args),
                        err_no = err_no,
                        err_msg = self._get_error_msg(),
                ))
            return val
        return checked_fn


    ######################
    ## Abstract Methods ##
    ######################

    def _get_error_no(self):
        """Gets the error status of an instrument. An error status of 0
        indicates the last instruction sent to the instrument executed without
        an error, and any other error code indicates that an error was raised.

        Returns:
          - int: 0 if there is no error. Anything else otherwise.
        """
        raise NotImplementedError

    def _get_error_msg(self):
        """Gets the error message of an instrument, assuming a non-zero error
        code.

        Returns:
          - str: An error message.
        """
        raise NotImplementedError

##########################
## Error String Formats ##
##########################

NONZERO_ERROR_NO = '{fn_name}({fn_args}) resulted in {cls_name} error ({err_no}): {err_msg}'

