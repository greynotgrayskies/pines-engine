"""
SR830 Lock-In Module

Importable:
  - SR830
"""

class SR830(DAQ, VisaInstrument):
    def _reset(self):
        pass

    def get_error_no(self):
        pass

    def get_error_msg(self):
        pass


    ####################
    ## SR830 Commands ##
    ####################

    def set_trigger_mode(self, mode):
        write_and_check_error(self, 'TSTR {0}'.format(mode))

    def set_output_interface(self, interface):
        write_and_check_error(self, 'OUTX {0}'format(interface))

    def trigger(self):
        write_and_check_error(self, 'TRIG')

    def get_value(self, channel):
        float(read_and_check_error(self, 'OUTP ? {0}'.format(channel)))

    def get_values(self, ch1, ch2, *args):
        if args:
            args = ',' + ','.join(args)
        else:
            args = ''
        vals = read_and_check_error(self, 'SNAP ? {0},{1}{2}'.format(ch1, ch2, args))
        return [float(val) for val in vals.split(',')]

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
        raise InstrumentError("Error reading '{0}' from SR830: {1}".format(
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
        raise InstrumentError("Error writing '{0}' to SR830: {1}".format(
                val, instrument.get_error_msg()))

