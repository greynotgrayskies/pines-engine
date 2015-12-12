"""

"""
import re

__all__ = ['Experiment', 'Parameter', 'IntParameter']

class Experiment(object):
    data_points = []
    instruments = {}
    parameters = {}

    def __init__(self, **kwargs):
        for param_name, param in self.parameters.items():
            setattr(self, param_name, param.parameterize(kwargs[param_name]))
        for instr_name, instr in self.instruments.items():
            pass

    def setup(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    @staticmethod
    def analyze(data):
        raise NotImplementedError

# TODO(Jeffrey): Type checking to prevent errors being raised in is_valid?
# Might also be better not to type check so that bugs won't go by unnoticed.

class Parameter(object):
    """Experiment parameter with

    Parameter ABC, used to check that the parameters values used to
    initialize an instrument satisfy defined conditions.

    Instance Attributes:
        name: A string containing the name of the Parameter.
    """
    def __init__(self, name):
        self.name = name

    def parameterize(self, param):
        param_val = self.str_to_param_value(param)
        self.is_valid(param_val)
        return param_val

    def is_valid(self, param_value):
        """Checks whether or not a value satisfies a parameter.

        Args:
            param_value: The parameter value.

        Returns:
            bool: True if the value satisfies the
        """
        raise NotImplementedError

    def str_to_param_value(self, param):
        raise NotImplementedError

class StringParameter(Parameter):
    """A string parameter.

    A Parameter which uses a regular expression pattern to check whether an
    inputted string is valid.

    Regular Expression Syntax:
    https://docs.python.org/2/library/re.html#regular-expression-syntax

    Instance Attributes:
        name: [inherited]
        regex: A regex object compiled from an inputted string.
    """
    def __init__(self, name, pattern):
        Parameter.__init__(self, name)
        self.regex = re.compile(pattern)

    def is_valid(self, param_value):
        return bool(self.regex.match(param_value))

    def str_to_param_value(self, param):
        return param

class IntParameter(Parameter):
    """An integer parameter.

    A Parameter which checks whether an inputted integer parameter is within a
    minimum and maximum bound. If min or max is set to None, then there is no
    minimum or maximum bound, respectively.

    Instance Attributes:
        name: [inherited]
        min: A numerical value specifying the minimum bound.
        max: A numerical value specifying the maximum bound.
    """
    def __init__(self, name, min=float('-inf'), max=float('inf')):
        Parameter.__init__(self, name)
        self.min = min
        self.max = max

    def is_valid(self, param_value):
        return self.min <= param_value <= self.max

    def str_to_param_value(self, param):
        try:
            return int(param)
        except ValueError:
            raise ParameterError('Could not convert "{0}" parameter value "{1}" to a int.'.format(self.name, param))

class FloatParameter(Parameter):
    """An floating point parameter.

    A Parameter which checks whether an inputted float parameter is within a
    minimum and maximum bound. If min or max is set to None, then there is no
    minimum or maximum bound, respectively.

    Instance Attributes:
        name: [inherited]
        min: A numerical value specifying the minimum bound.
        max: A numerical value specifying the maximum bound.
    """
    def __init__(self, name, min=float('-inf'), max=float('inf')):
        Parameter.__init__(self, name)
        self.min = min
        self.max = max

    def is_valid(self, param_value):
        return self.min <= param_value <= self.max

    def str_to_param_value(self, param):
        try:
            return float(param)
        except ValueError:
            raise ParameterError('Could not convert "{0}" parameter value "{1}" to a float.'.format(self.name, param))

class OptionParameter(Parameter):
    """A parameter with options.

    A Parameter which predefines a set of options that are valid.

    Instance Attributes:
        name: [inherited]
        options: A list of strings containing valid options
    """
    def __init__(self, name, options):
        Parameter.__init__(self, name)
        self.options = options

    def is_valid(self, param_value):
        return param_value in self.options

    def str_to_param_value(self, param):
        return param

class ParameterError(Exception):
    pass

class ExperimentError(Exception):
    pass
