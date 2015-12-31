from instrument import *
from instrument.mwfreqsynth import *
from instrument.lib.visainstrument import *
import visa

class HP8673C(MWFreqSynth, VisaInstrument):
    def _reset(self):
        pass

    def _get_error_no(self):
        return self.get_error_no_inst()

    def _get_error_msg(self):
        return ''

    ######################
    ## HP8673C Commands ##
    ######################

    # TODO(Jeffrey): Temporary, until I figure out how the commands are
    # formatted

    def get_error_no_inst(self):
        return int(self._read('MG'))

    @VisaInstrument.check_error
    def set_amp(self, val):
        self._write('AP {0} DM'.format(val))

    @VisaInstrument.check_error
    def set_freq(self, val):
        self._write('FR {0} MZ'.format(val))

    @VisaInstrument.check_error
    def power_on(self, val):
        self._write('RF1')

    @VisaInstrument.check_error
    def power_off(self, val):
        self._write('RF0')

