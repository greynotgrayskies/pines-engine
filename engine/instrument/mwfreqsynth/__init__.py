"""
Microwave Frequency Synthesizer Module

The microwave frequency synthesizer module, which contains the microwave

Importable:
  - MWFreqSynth
"""
from instrument import *

__all__ = ['MWFreqSynth']

class MWFreqSynth(Instrument):
    def get_power(self):
        raise NotImplemented()

    def set_power(self, power, unit):
        raise NotImplemented()

    def get_freq(self):
        raise NotImplemented()

    def set_freq(self, freq, unit):
        raise NotImplemented()

