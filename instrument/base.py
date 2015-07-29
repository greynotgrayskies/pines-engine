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
    mapping values for each parameter.

    Class Attribute:
        _instructions (dict): A mapping of names to Instructions.
        _parameters (dict): A mapping of names to parameters.

    Instance Attributes:
        _connected (bool): Indicates whether the instrument is connected.
        _engine (Engine): The experiment engine

    Parameters:
        address (str): The hardware address

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
    _parameters = {
        'address': StringParameter('Address', '.+'),
    }

    def __init__(self, engine, **kwargs):
        self._engine = engine
        self._connected = False
        self._instr = None

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
        return self._scope_attributes('_parameters')


    #####################
    ## Private Methods ##
    #####################

    def _scope_attributes(self, attr):
        all_attrs = dict(getattr(self, attr))
        cls = type(self).__bases__[0]
        # TODO(Jeffrey): Should probably support multiple inheritance after all
        while cls is not object:
            if not hasattr(cls, attr):
                raise InstrumentError('{0} class has no "{1}" attribute. Check definitition file and make sure that the class has "{1}" defined.'.format(cls.__name, attr))
            superclass_attrs = getattr(cls, attr)
            for key in superclass_attrs:
                if key not in all_attrs:
                    all_attrs[key] = superclass_attrs[key]
            cls = cls.__bases__[0]
        return all_attrs
                

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
