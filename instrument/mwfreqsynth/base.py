from instrument.base import *

class MWFreqSynth(Instrument):
    parameters = {
        'freq':         Parameter(  'Frequency',
                                    UndefinedDomain()),
        'freq_unit':    Parameter(  'Frequency Unit',
                                    UndefinedDomain()),
        'amp':          Parameter(  'Amplitude',
                                    UndefinedDomain()),
        'amp_unit':     Parameter(  'Amplitude Unit',
                                    UndefinedDomain()),
    }

    def get_power(self):
        raise NotImplemented()

    def set_power(self, power):
        raise NotImplemented()

    def get_freq(self):
        raise NotImplemented()

    def set_freq(self, freq):
        raise NotImplemented()
