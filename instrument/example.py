"""
Example Instrument
"""
# All instruments should have this import statement
from instrument.base import *

class ExampleInstrument(Instrument):
    def connect(self):
        print('Connected')

    def disconnect(self):
        print('Disconnected')

    def setup(self):
        print('Set up')

    def read(self):
        print('Reading')

    def write(self):
        print('Writing')
