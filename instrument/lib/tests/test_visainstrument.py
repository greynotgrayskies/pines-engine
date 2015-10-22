from instrument.lib.visainstrument import VisaInstrument
import unittest

from collections import defaultdict
import importlib
import visa

class TestVisaInstrumentCommunication(unittest.TestCase):
    def setUp(self):
        # Modify visa interface so that we don't need actual hardware.
        visa.ResourceManager = DummyVisaResourceManager

    def tearDown(self):
        # Reload visa library after running tests.
        importlib.reload(visa)

    def test_visa_instrument_communication(self):
        # Initialize a SimpleVisaInstrument
        instr = SimpleVisaInstrument(address='12345')
        instr._connect()
        resource = instr._resource

        instr._read('read instruction')
        self.assertEqual(resource.get_last_instruction(), 'read instruction')
        instr._write('write instruction')
        self.assertEqual(resource.get_last_instruction(), 'write instruction')

        # Disconnect instrument
        instr._disconnect()

    def test_visa_instrument_communication_with_error_checking(self):
        # Initialize a SimpleVisaInstrument
        instr = SimpleVisaInstrument(address='12345')
        instr._connect()
        resource = instr._resource

        instr.test_query_instruction()
        self.assertEqual(resource.get_last_instruction(), 'test query instruction')
        instr.test_write_instruction()
        self.assertEqual(resource.get_last_instruction(), 'test write instruction')

        # TODO(Jeffrey): Need to test error handling. Don't have access to
        # pydocs, so I don't remember what the assert function was.

        # Disconnect instrument
        instr._disconnect()

class SimpleVisaInstrument(VisaInstrument):
    def __init__(self, **kwargs):
        VisaInstrument.__init__(self, **kwargs)
        self.error_code = 0
        self.error_msg = 'No Error'

    def _get_error_no(self):
        return self.error_code

    def _get_error_msg(self):
        return self.error_msg
    
    def test_query_instruction(self):
        return self._read('test query instruction')
    
    def test_write_instruction(self):
        return self._write('test write instruction')


####################
## Visa Utilities ##
####################

# Utilities to interface with the `pyvisa` module without any actual hardware.

class DummyVisaResourceManager(object):
    """Dummy Visa Resource Manager interface, used to check for valid read and
    write commands.
    """
    opened_resources = set()

    @staticmethod
    def open_resource(address):
        #assert address not in TestResourceManager.opened_resources
        DummyVisaResourceManager.opened_resources.add(address)
        return DummyResource(address)
    
class DummyResource(object):
    """Dummy Visa Resource interface."""
    def __init__(self, addr):
        self.addr = addr
        self.query_vals = defaultdict(lambda: '')
        self.last_instruction = None
        self.connected = True

    def close(self):
        """Closes communications with an instrument"""
        #DummyVisa.opened_resources.remove(self.address)
        self.connected = False

    def query(self, instruction):
        """Simulates sending a query instruction to an instrument. The return
        value is specified by the `query_vals` dictionary, which can be used to
        return custom values if necessary.
        """
        if self.connected:
            self.set_last_instruction(instruction)
            return self.query_vals[instruction]
        raise visa.VisaIOError('Instrument has been disconnected.')

    def write(self, instruction):
        """Simulates writing an instruction to an instrument"""
        if self.connected:
            self.set_last_instruction(instruction)
            return
        raise visa.VisaIOError('Instrument has been disconnected.')

    def set_last_instruction(self, instruction):
        """Saves instruction, if an instruction hasn't been already saved. We
        don't want to save the last instruction sent since often we query for
        an error right after an instruction.
        """
        if self.last_instruction is None:
            self.last_instruction = instruction

    def get_last_instruction(self):
        """Returns the previously saved instruction string sent to this
        instrument.
        """
        instruction = self.last_instruction
        self.last_instruction = None
        return instruction

