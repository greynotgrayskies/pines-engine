"""
CInstrument Module

CInstrument module, which contains utilities for interfacing with instruments
with predefined C libraries.

Importable:
  - CInstrument
"""

from instrument import *
from ctypes import *

__all__ = ['CInstrument']

class CInstrument(Instrument):
    """C Instrument Interface.

    The C Instrument Interface, which needs a better docstring.

    Parameters:
      - libpath (str): Path to a DLL file
      - functions (dict[str -> (str, tuple[str])]): A dictionary of function
        names mapped to `restype`, `argtypes` pairs
        ...

    Instance Attributes:
        ...

    Class Attributes:
      - _lib (CLibrary):
        ...
    """

    @classmethod
    def loadDLL(cls, libpath, functions):
        """Loads a DLL to the `_lib` attribute of a class.

        This method must be called after a CInstrument is defined.

        Args:
          - libpath (str): Path to a DLL file
          - functions (dict[str -> (str, tuple[str])]): A dictionary of function
            names mapped to `restype`, `argtypes` pairs
        """
        try:
            cls._lib = CDLL(libpath)
        except OSError as e:
            raise InstrumentError("cannot load file at '{0}': {1}".format(libpath, e.args[0]))
        for fn_name, types in functions.items():
            fn = getattr(cls._lib, fn_name)
            fn.restype = types[0]
            fn.argtypes = types[1]

