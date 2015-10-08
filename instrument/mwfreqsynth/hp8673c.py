from instrument import *
from instrument.mwfreqsynth import *
from instrument.lib.visainstrument import *
import visa

class HP8673C(MWFreqSynth, VisaInstrumnet):
    def _reset(self):
        pass

    def get_error_no(self):
        return 0

    def get_error_msg(self):
        return ''

    ######################
    ## HP8673C Commands ##
    ######################

    # TODO(Jeffrey): Temporary, until I figure out how the commands are
    # formatted

    def set_amplitude(self, val):
        write_and_check_error('AP {0} DM'.format(val))

    def set_freq(self, val):
        write_and_check_error('FR {0} MZ'.format(val))

    def power_on(self, val):
        write_and_check_error('RF1')

    def power_off(self, val):
        write_and_check_error('RF0')

#####################
## Private methods ##
#####################

def read_and_check_error(instrument, val):
    """Read from an instrument and check for an error. If an error is
    encountered, an InstrumentError is raised.
    """
    val = instrument._read(val)
    if instrument.get_error_no() != 0:
        # Reprocure error message, since checking clears it
        instrument._read(val)
        raise InstrumentError("Error reading '{0}' from HP8673C: {1}".format(
                val, instrument.get_error_msg()))
    return val

def write_and_check_error(instrument, val):
    """Write to an instrument and check for an error. If an error is
    encountered, an InstrumentError is raised.
    """
    instrument._write(val)
    if instrument.get_error_no() != 0:
        # Reprocure error message, since checking clears it
        instrument._write(val)
        raise InstrumentError("Error writing '{0}' to HP8673C: {1}".format(
                val, instrument.get_error_msg()))

