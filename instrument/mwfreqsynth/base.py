from instrument.base import *

class MWFreqSynth(Instrument):
    parameters = {
        'freq':         UndefinedParameter('Frequency'),
        'freq_unit':    UndefinedParameter('Frequency Unit'),
        'amp':          UndefinedParameter('Amplitude'),
        'amp_unit':     UndefinedParameter('Amplitude Unit'),
    }

    def get_power(self):
        raise NotImplemented()

    def set_power(self, power):
        raise NotImplemented()

    def get_freq(self):
        raise NotImplemented()

    def set_freq(self, freq):
        raise NotImplemented()
