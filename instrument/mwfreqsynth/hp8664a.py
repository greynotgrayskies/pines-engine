from instrument.mwfreqsynth.base import *
#import visa

class HP8664A(MWFreqSynth):

    def get_freq(self):
        self._write(self.instructions['get_freq'])

    def set_freq(self):
        self._write(self.write_instruction)

    parameters = {
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

    instructions = {
        'set_freq':     Instruction('FREQ:CW {freq}{freq_unit}'),
        'get_freq':     Instruction('FREQ:CW?')
    }
