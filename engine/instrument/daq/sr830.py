"""
SR830 Lock-In Module

Importable:
  - SR830
"""

from instrument import *
from instrument.daq import *
from instrument.lib.visainstrument import *
import visa

class SR830(DAQ, VisaInstrument):
    def _reset(self):
        self.reset_inst()

    def _get_error_no(self):
        return self.get_error_status_inst()

    def _get_error_msg(self):
        return ''


    ####################
    ## SR830 Commands ##
    ####################

    def reset_inst(self):
        self._write('*RST')

    def get_error_status_inst(self):
        return int(self._write('ERRS?'))

    @VisaInstrument.check_error
    def set_trigger_mode(self, mode):
        self._write('TSTR {0}'.format(mode))

    @VisaInstrument.check_error
    def set_output_interface(self, interface):
        self._write('OUTX {0}'.format(interface))

    @VisaInstrument.check_error
    def trigger(self):
        self._write('TRIG')

    @VisaInstrument.check_error
    def get_value(self, channel):
        return float(self._read('OUTP ? {0}'.format(channel)))

    @VisaInstrument.check_error
    def get_values(self, ch1, ch2, *args):
        if args:
            args = ',' + ','.join(args)
        else:
            args = ''
        vals = self._read('SNAP ? {0},{1}{2}'.format(ch1, ch2, args))
        return [float(val) for val in vals.split(',')]

