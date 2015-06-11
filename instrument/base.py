"""
Instrument Module

Contains abstract base class, Instrument, which all instruments should inherit
from.
"""
import json
import re

#__all__ = ['Instrument', 'InstrumentError']

#TODO: Error Handling

###########################
## Instrument Definition ##
###########################

class Instrument(object):
    # TODO: Unintuitive to read and write. Need to find a better way to define
    # instrument parameters.
    #   - Initializing a class maybe?
    parameters = {
        'address':      Parameter(  'Address',
                                    StringDomain('.+')),
    }

    def __init__(self, **kwargs):
        cls = type(self)

        # TODO: Clearer implementation?
        while cls is not object:
            for param in cls.parameters:
                if param.name in self.__dict__:
                    continue
                if param.name in kwargs:
                    if param.is_valid(kwargs[param.name]):
                        setattr(self, param, kwargs[param])
                    else:
                        raise ParameterError('Invalid value assigned to parameter "{0}": {1}'.format(param.name, kwargs[param]))
                else:
                    raise ParameterError('Undefined parameter: {0}'.format(param.name))
            # Need to support multiple inheritance?
            cls = cls.__bases__[0]

    def _read(self, string):
        raise NotImplemented()

    def _write(self, string):
        raise NotImplemented()

    def _connect(self):
        raise NotImplemented()

    def _disconnect(self):
        raise NotImplemented()

    def _reset(self):
        raise NotImplemented()

    def _execute_instruction(self, instruction):
        raise NotImplemented()

##########################
## Parameter Definition ##
##########################

class Parameter(object):
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

    def is_valid(self, param_value):
        return param_value is None or param_value in self.domain

class Domain(object):
    pass

class UndefinedDomain(Domain):
    def __init__(self):
        self.type = None

    def  __contains__(self, item):
        return False

class StringDomain(Domain):
    def __init__(self, pattern):
        self.type = str
        self.pattern = re.compile(pattern)

    def __contains__(self, item):
        return bool(self.pattern.match(str(item)))

class IntDomain(Domain):
    def __init__(self, min, max):
        self.type = int
        self.min = min
        self.max = max

    def __contains__(self, item):
        return self.min <= self.type(item) <= self.max

class FloatDomain(Domain):
    def __init__(self, min, max):
        self.type = float
        self.min = min
        self.max = max

    def __contains__(self, item):
        return self.min <= self.type(item) <= self.max

class SetDomain(Domain):
    def __init__(self, type, lst):
        self.type = type
        self.lst = [self.type(el) for el in lst]
        self.lst.sort()

    def __contains__(self, item):
        return self.type(item) in lst

class CompoundDomain(Domain):
    def __init__(self, *domains):
        self.domains = domains

    def __contains__(self, item):
        for domain in self.domains:
            if item in domain:
                return True
        return False

##########################
## Machine Instructions ##
##########################

class Instruction(object):
    def __init__(self, instruction_format, param_list):
        self.instruction_format = instruction_format
        self.param_list = param_list

    def instruction_string(self, instrument):
        args = [getattr(instrument, param) for param in param_list]
        return self.instruction_format.format(*args)

################
## Exceptions ##
################

class InstrumentError(Exception):
    pass

class ParameterError(Exception):
    pass
