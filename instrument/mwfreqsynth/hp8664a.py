from instrument.mwfreqsynth.base import *
from instrument.lib.visainstrument import VisaInstrument
import visa

# TODO(Jeffrey): Multiple Inheritance may actually be useful. We could create a
# VISA instrument, which would have connect, disconnect, read and write
# defined. It shouldn't have parameters though?
class HP8664A(MWFreqSynth, VisaInstrument):
    def _reset(self):
        # TODO: What exactly needs to be done to reset this anyways?
        pass

    def get_freq(self):
        return float(self._read(self._instruction_str('freq_get')))

    def set_freq(self):
        self._write(self._instruction_str('freq_set'))

    # TODO(Jeffrey): No reason for parameter and its unit to be considered
    # separately. Combine possibly?
    _parameters = {
        'amp':          FloatParameter('Amplitude', 0.0, 1000.0),
        'amp_unit':     OptionParameter('Amplitude Unit', [
                            'dBmW',
                            'dBuV',
                            'V',
                            'mV',
                            'uV',
                        ]),
        'freq':         FloatParameter('Frequency', 0.1, 3000.0),
        'freq_unit':    OptionParameter('Frequency Unit', [
                            'HZ',
                            'KHZ',
                            'MHZ',
                            'GHZ',
                        ]),
        'opmode':       OptionParameter('Operation Mode', [
                            'Continuous Wave',
                            'Pulse',
                            'Sweep',
                        ]),
    }

    _instructions = {
        'amp_set':      'AMP {amp}{amp_unit}',
        'amp_unit_set': 'AMP:UNIT {amp_unit}',
        'check_error':  'SYST:ERR? STR',
        'freq_set':     'FREQ:CW {freq}{freq_unit}',
        'freq_get':     'FREQ:CW?',
    }
