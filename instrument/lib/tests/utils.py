"""
Instrument Library Test Utilities
"""

import instrument.lib.visainstrument

def harness_visa_instrument(inst):
    """Harnesses a VisaInstrument instrument for testing."""
    inst.visa = DummyVisa

class DummyVisa(object):
    """Dummy Visa module interface, used to check for valid read and write
    commands."""
    opened_resources = set()

    @classmethod
    def open_resource(address):
        #assert address not in TestResourceManager.opened_resources
        DummyVisa.opened_resources.add(address)
        return DummyResource(addr)

    class VisaIOError(Exception):
        pass
    
class DummyResource(object):
    """Dummy Visa Resource interface."""
    def __init__(self, addr):
        self.addr = addr
        self.query_vals = defaultdict(lambda: '')
        self.last_instruction = None
        self.connected = True

    def close(self):
        #DummyVisa.opened_resources.remove(self.address)
        self.connected = False

    def query(self, instruction):
        if self.connected:
            self.set_last_instruction(instruction)
            return self.query_vals[instruction]

    def write(self, instruction):
        if self.connected:
            self.set_last_instruction(instruction)

    def set_last_instruction(self, instruction):
        """Saves instruction, if an instruction hasn't been already saved."""
        if self.last_instruction is None:
            self.last_instruction = instruction

    def last_instruction_matches(instruction):
        """Returns True if INSTRUCTION matches the last saved instruction
        written to this instrument."""
        matches = instruction == self.last_instruction
        self.last_instruction = None
        return matches

