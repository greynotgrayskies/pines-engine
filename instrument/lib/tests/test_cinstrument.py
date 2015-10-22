from instrument.lib.cinstrument import CInstrument
import unittest

import ctypes
import importlib

# TODO(Jeffrey): I really don't like this test. It might be a good idea to
# avoid using compiled C libraries to test this, but is this a good approach?
# Since we're not using any DLL files, then we can't even check that we're
# using the ctypes module correctly.
#
# We can also just use a Makefile to compile the C library when testing using
# Travis. And then just skip this test if the C library cannot be found.
#
# Maybe the CInstrument implementation can also be refactored a bit. But later.

class TestCInstrument(unittest.TestCase):
    def setup(self):
        ctypes.CDLL = DummyCDLL

    def tearDown(self):
        importlib.reload(ctypes)

    # This test is pretty worthless
    def test_cinstrument(self):
        ctypes.CDLL = DummyCDLL
        SimpleCInstrument.loadDLL('arithmetic', {})
        self.assertEqual(SimpleCInstrument.add(1, 2), 3)
        instr = SimpleCInstrument()
        self.assertEqual(instr.add(1, 2), 3)


###############
## Utilities ##
###############

class DummyCDLL(object):
    """Dummy DLL object.

    Write a better docstring, pls.
    """
    def __init__(self, path):
        for name, fn in FUNCTIONS[path].items():
            setattr(self, name, fn)

def c_add(a, b):
    assert type(a) is ctypes.c_int
    assert type(b) is ctypes.c_int
    #return ctypes.c_int(a.value + b.value)
    return a.value + b.value

FUNCTIONS = {
    'arithmetic': {
        'add': c_add,
    }
}

class SimpleCInstrument(CInstrument):
    @staticmethod
    def add(a, b):
        return SimpleCInstrument._lib.add(
                ctypes.c_int(a),
                ctypes.c_int(b),
        )

