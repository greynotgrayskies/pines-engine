from instrument.mwfreqsynth.base import *
import visa

class HP8664A(MWFreqSynth):

    def get_freq(self):
        self._write(self.instructions['get_freq'])

    def set_freq(self):
        self._write(self.write_instruction)

    parameters = {
        'freq':         Parameter(  'Frequency',
                                    SpectrumDomain(float, 0.1, 3000)),
        'freq_unit':    Parameter(  'Frequency Unit',
                                    SetDomain(str, [
                                            'HZ',
                                            'KHZ',
                                            'MHZ',
                                            'GHZ',
                                    ])),
        'amp':          Parameter(  'Amplitude',
                                    SpectrumDomain(float, 0, 1000)),
        'amp_unit':     Parameter(  'Amplitude Unit',
                                    SetDomain(str, [
                                            'dBmW',
                                            'dBuV',
                                            'V',
                                            'mV',
                                            'uV',
                                    ])),
        'opmode':       Parameter(  'Operation Mode',
                                    SetDomain(str, [
                                            'Continuous Wave',
                                            'Pulse',
                                            'Sweep',
                                    ])),
    }

    instructions = {
        'set_freq':     Instruction('FREQ:CW {0}{1}', ['freq', 'freq_unit']),
        'get_freq':     Instruction('FREQ:CW?', [])
    }
