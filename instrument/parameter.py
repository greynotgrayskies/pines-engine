import re

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

    def is_valid(self, param_value):
        """Checks whether or not a value satisfies a parameter.

        Args:
            param_value: the value being passed in.

        Returns:
            bool: True if the value satisfies the
        """
        raise NotImplemented()

class UndefinedParameter(Parameter):
    """An undefined parameter.

    An undefined Parameter, which should be used to indicate that it should be
    overriden by a child class.

    Instance Attributes:
        name: [inherited]
    """
    def __init__(self, name):
        super().__init__(name)

    def is_valid(self, param_value):
        raise ParameterError('Parameter bounds not defined.')

class StringParameter(Parameter):
    """A string parameter.

    A Parameter which uses a regular expression pattern to check whether an
    inputted string is valid.

    Regular Expression Syntax:
    https://docs.python.org/2/library/re.html#regular-expression-syntax

    Instance Attributes:
        name: [inherited]
        regex: A regex object compiled from an inputted string.

    >>> param = StringParameter('Parameter', '[A-Za-z]+')
    >>> param.is_valid('Test')
    True
    >>> param.is_valid('123')
    False
    >>> param.is_valid('')
    False
    """
    def __init__(self, name, pattern):
        super().__init__(name)
        self.regex = re.compile(pattern)

    def is_valid(self, param_value):
        if not isinstance(param_value, str):
            return False
        return bool(self.regex.match(param_value))

class IntParameter(Parameter):
    """An integer parameter.

    A Parameter which checks whether an inputted integer parameter is within a
    minimum and maximum bound. If min or max is set to None, then there is no
    minimum or maximum bound, respectively.

    Instance Attributes:
        name: [inherited]
        min: A integer specifying the minimum bound, or None if no such bound.
        max: A integer specifying the maximum bound, or None if no such bound.
    """
    def __init__(self, name, min=None, max=None):
        super().__init__(name)
        self.min = min
        self.max = max

    def is_valid(self, param_value):
        return self.min <= int(param_value) <= self.max

class FloatParameter(Parameter):
    """An floating point parameter.

    A Parameter which checks whether an inputted float parameter is within a
    minimum and maximum bound. If min or max is set to None, then there is no
    minimum or maximum bound, respectively.

    Instance Attributes:
        name: [inherited]
        min: A float specifying the minimum bound, or None if no such bound.
        max: A float specifying the maximum bound, or None if no such bound.

    >>> param = IntParameter('Parameter', max=10.0) # Max bound 10, no min bound
    >>> param.is_valid(1000)
    False
    >>> param.is_valid(-1000)
    True
    """
    def __init__(self, name, min, max):
        super().__init__(name)
        self.min = min
        self.max = max

    def is_valid(self, param_value):
        return self.min <= float(param_value) <= self.max

class OptionParameter(Parameter):
    """A parameter with options.

    A Parameter which predefines a set of options that are valid.

    Instance Attributes:
        name: [inherited]
        options: A list of strings containing valid options
    """
    def __init__(self, name, options):
        super().__init__(name)
        self.options = options

    def is_valid(self, param_value):
        return param_value in self.options

# Is this necessary?
class CompoundParameter(Parameter):
    def __init__(self, name, parameters):
        super().__init__(name)
        self.parameters = parameters

    def is_valid(self, param_value):
        for domain in self.parameters:
            if param_value in domain:
                return True
        return False
