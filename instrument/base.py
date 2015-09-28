"""
Instrument Module

Contains Instrument interface, which all instruments should inherit from.

Importable:
  - Instrument
  - InstrumentError
"""
from instrument.parameter import *

# TODO(Jeffrey): Error Handling

# TODO(Jeffrey): Consider defining errors with long names elsewhere, so that
# they don't clutter the code?

###########################
## Instrument Definition ##
###########################

class Instrument(object):
    """Instrument interface.

    The Instrument object interface, which all instrument definitions should
    inherit from. All instruments 
    The attributes of an Instrument should be defined in a class
    attribute named `parameters`. If a child class has a parameter name that
    conflicts with that of an ancestor class, then the parameter of the child
    will override the ancestor parameter.

    To instantiate an Instrument, pass in a dictionary of keyword arguments
    mapping values for each parameter.

    Instance Attributes:
        _connected (bool): Indicates whether the instrument is connected.
        _engine (Engine): The experiment engine

    Parameters:
        engine (Engine): The experiment engine
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


    #####################
    ## Utility Methods ##
    #####################

    def _instruction_str(self, instruction_name):
        """Retrieves a formatted instruction string for an instrument. This
        method will look up an instruction in the `_instructions` dictionary,
        and format it with the current instrument settings.

        Args:
            instruction_name (str): The instruction name

        Returns:
            str: A formatted instruction
        """
        return self._instructions[instruction_name].format(**self.__dict__)


##########################
## Machine Instructions ##
##########################

class Instruction(object):
    """A machine instruction.

    An abstraction for raw machine instructions that require arguments.
    Facilitates formatting an instruction into a string, by taking a string
    specifying the format of the instruction as well as which parameters of an
    instrument are required.

    Instance Attributes:
        format: The format of an instruction

    >>> instrument = ExampleInstrument(address='123', value=100)
    >>> instruct = Instruction('arg0: {address}; arg1: {value}')
    >>> instruct.to_string(instrument)
    'arg0: 123; arg1: 100'
    """
    def __init__(self, format):
        self.format = format

    def to_string(self, instrument):
        return self.format.format(**instrument.__dict__)

################
## Exceptions ##
################

class InstrumentError(Exception):
    """Base exception raised by instruments."""
    pass

####################
## Error Messages ##
####################


###########
## Other ##
###########

__all__ = ['Instrument', 'InstrumentError']

