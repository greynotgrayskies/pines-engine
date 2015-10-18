from instrument.lib.visainstrument import VisaInstrument
import unittest

from collections import defaultdict
import importlib
import visa

class TestVisaInstrumentCommunication(unittest.TestCase):
    def setUp(self):
        # Modify visa interface so that we don't need actual hardware.
        visa.ResourceManager = TestResourceManager

    def tearDown(self):
        # Reload visa library after running tests.
        importlib.reload(visa)

    def test_visa_instrument_communication(self):


###############
## Utilities ##
###############

class TestInstrument(VisaInstrument):
    def __init__(self, addr):
        VisaInstrument.__init__(self):

