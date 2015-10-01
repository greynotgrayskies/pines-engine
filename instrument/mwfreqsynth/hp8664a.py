from instrument.mwfreqsynth import *
from instrument.lib.visainstrument import VisaInstrument
import visa

class HP8664A(MWFreqSynth, VisaInstrument):
    def _setup(self):
        pass

    def _reset(self):
        # TODO: What exactly needs to be done to reset this anyways?
        pass

    def get_freq(self):
        return float(self._read(self._instruction_str('freq_get')))

    def set_freq(self, freq=None):
        if freq is not None:
            self.freq = freq
        self._write(self._instruction_str('freq_set'))

    _parameters = {
        'amp':          FloatParameter('Amplitude'),
        'amp_unit':     OptionParameter(
                            'Amplitude Unit',
                            [
                                'dBmV',
                                'dBuV',
                                'V',
                                'mV',
                                'uV',
                            ],
                        ),
        'freq':         FloatParameter('Frequency'),
        'freq_unit':    OptionParameter(
                            'Frequency Unit',
                            [
                                'HZ',
                                'KHZ',
                                'MHZ',
                                'GHZ',
                            ],
                        ),
        'opmode':       OptionParameter(
                            'Operation Mode',
                            [
                                'Continuous Wave',
                                'Pulse',
                                'Sweep',
                            ],
                        ),
    }

    _instructions = {
        'amp_set':      'AMP {amp}{amp_unit}',
        'amp_unit_set': 'AMP:UNIT {amp_unit}',
        'check_error':  'SYST:ERR? STR',
        'freq_set':     'FREQ:CW {freq}HZ',
        'freq_get':     'FREQ:CW?',
    }
