"""
Instrument Module

Contains abstract base class, Instrument, which all instruments should inherit
from.
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

    The Instrument object interface, which all hardware definitions should
    inherit from. The attributes of an Instrument should be defined in a class
    attribute named `parameters`. If a child class has a parameter name that
    conflicts with that of an ancestor class, then the parameter of the child
    will override the ancestor parameter.

    To instantiate an Instrument, pass in a dictionary of keyword arguments
    mapping values for each parameter. The

    Class Attribute:
        instructions: A dictionary mapping instruction names to Instructions.
        parameters: A dictonary of parameters

    Instance Attributes:
        address: A string containing the hardware address

    Abstract Methods:
        _read
        _write
        _connect
        _disconnect
        _reset

    >>> instrument1 = Instrument(address='123')
    >>> # Can also be initialized this way:
    >>> kwargs = {address: '789'}
    >>> instrument2 = Instrument(**kwargs)
    >>> instrument1.address
    '123'
    >>> instrument2.address
    '789'
    """
    instructions = {}
    # TODO(Jeffrey): Unintuitive to read and write. Need to find a better way to
    # define instrument parameters.
    #   - Initializing a class maybe?
    parameters = {
        'address': StringParameter('Address', '.+'),
    }

    def __init__(self, **kwargs):
        all_params = self._all_parameters()

        if set(all_params.keys()) != set(kwargs.keys()):
            for param in all_params.keys():
                if param not in kwargs:
                    raise ParameterError('Undefined parameter: {0}'.format(param))
            extra_params = set(kwargs.keys())
            for param in all_params:
                extra_params.remove(param)
            raise ParameterError('Extra parameters passed when initializing {0} object: {1}'.format(type(self).__name__, list(extra_params)))

        for name in all_params:
            if not all_params[name].is_valid(kwargs[name]):
                raise ParameterError('Invalid value assigned to parameter "{0}": "{1}"'.format(name, kwargs[name]))
            setattr(self, name, kwargs[name])


    ######################
    ## Abstract Methods ##
    ######################

    def _read(self, string):
        """Reads from an instrument."""
        # Perhaps this should be implemented by a child class?
        raise NotImplemented()

    def _write(self, string):
        """Writes to an instrument."""
        # Perhaps this should be implemented by a child class?
        raise NotImplemented()

    def _connect(self):
        """Connect to and set up an instrument. Will always be called at the
        beginning of an experiment."""
        raise NotImplemented()

    def _disconnect(self):
        """Terminates a connection to an instrument. Will always be called at
        the end of an experiment."""
        raise NotImplemented()

    def _reset(self):
        """Resets an instrument. Performs a sequence of actions that will allow
        an instrument to perform a different function.
        """
        raise NotImplemented()

    ###################
    ## Other Methods ##
    ###################

    def _execute_instruction(self, instruction_name):
        """Instructs an instrument to execute an instruction. This method will
        look for an attribute `instructions` which is a dictionary mapping an
        instruction name to an Instruction object, that should be defined

        Args:
            instruction name: A string of the instruction name

        Returns:
            The value that the instruction would return
        """
        raise NotImplemented()

    def _all_parameters(self):
        """Returns a dictionary of all parameters of a class. This dictionary is
        formed iterating through all ancestor classes, and combining all the
        parameter dictionaries. If a child class and an ancestor class have
        conflicting parameter names, then the child parameter is given
        preference.

        Note: This implementation does not support instruments inheriting from
        multiple classes, since the handling conflicting parameter names in this
        case would not be well-defined anyways.

        Returns:
            A dictionary mapping parameter strings to Parameter objects.
        """
        all_params = dict(self.parameters)
        cls = type(self).__bases__[0]
        while cls is not object:
            if not hasattr(cls, 'parameters'):
                raise SyntaxError('{0} class has no "parameter" attribute. Check definition file and make sure that the class has "parameter" defined.'.format(cls.__name__))
            for param in cls.parameters:
                if param in all_params:
                    continue
                else:
                    all_params[param] = cls.parameters[param]
            cls = cls.__bases__[0]
        return all_params


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
    >>> instruct = Instrument('arg0: {address}; arg1: {value}')
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
    pass

class ParameterError(Exception):
    pass

####################
## Error Messages ##
####################


###########
## Other ##
###########

# Definitions that will be loaded with `from instrument.base import *`
__all__ = ['Instrument', 'Parameter', 'UndefinedParameter', 'StringParameter',
    'IntParameter', 'FloatParameter', 'OptionParameter', 'CompoundParameter',
    'Instruction', 'InstrumentError', 'ParameterError']
