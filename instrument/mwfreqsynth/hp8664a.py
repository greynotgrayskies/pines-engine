from instrument import *
from instrument.mwfreqsynth import *
from instrument.lib.visainstrument import *
import visa

class HP8664A(MWFreqSynth, VisaInstrument):
    def _reset(self):
        # TODO: What exactly needs to be done to reset this anyways?
        pass

    def get_freq(self):
        return float(self._read(self._instruction_str('freq_get')))

    def set_freq(self, freq=None):
        if freq is not None:
            self.freq = freq
        self._write(self._instruction_str('freq_set'))

    def get_error_no(self):
        pass

    def get_error_msg(self):
        pass


    ######################
    ## HP8664A Commands ##
    ######################

    # TODO(Jeffrey): Double check get commands. The read might return the value
    # in weird string formats.

    ##################
    ## AM Subsystem ##
    ##################

    def get_am_depth(self):
        """Gets the AM depth in percent.

        *RST value is 0%.

        Returns:
          - float: AM depth in percent.
        """
        val = self._read('AM:DEPTH?')
        self.check_error()
        return val

    def set_am_depth(self, val):
        """Sets the AM depth in percent.

        Can also set the AM depth to the 'MIN' or 'MAX' AM depth.
        
        Parameters:
         - val (float/str): AM depth in percent.
        """
        self._write('AM:DEPTH {0}'.format(val))
        self.check_error()

    def get_am_depth_step(self):
        """Returns the AM depth step size in percent.

        *RST value is 1%.

        Returns:
          - float: AM depth step size in percent.
        """
        val = self._read('AM:DEPTH:STEP:INCR?')
        self.check_error()
        return val

    def set_am_depth_step(self, val):
        """Sets the AM depth size in percent.

        Can also set the AM depth step size to the 'MIN' or 'MAX' AM depth step
        size.

        Parameters:
          - val (float/str): AM depth step size in percent.
        """
        self._write('AM:DEPTH:STEP:INCR {0}'.format(val))
        self.check_error()

    def get_AM_state(self):
        """Returns the AM modulation state, which is either 'ON' (1) or 'OFF'
        (0).

        *RST value is 'OFF'.

        Returns:
          - float: AM modulation state.
        """
        val = self._read('AM:STAT?')
        self.check_error()
        return val

    def set_AM_state(self, val):
        """Sets the AM modulation state, which is either 'ON' (1) or 'OFF' (0).

        Parameters:
          - val (float/str): AM modulation state.
        """
        self._write('AM:STAT {0}'.format(val))
        self.check_error()

    def get_AM_source(self):
        """Returns the AM source.

        *RST value is 'INT'.

        Returns:
          - str: AM source.
        """
        val = self._read('AM:SOUR?')
        self.check_error()
        return val

    def set_AM_source(self, val):
        """Sets the AM source: 'EXTernal' or 'INTernal'. 'INTernal,EXTernal' is
        accepted but will cause an execution error since the Signal Generator
        does not use both the internal audio source and an external audio
        source at the same time..

        Parameters:
          - val (str): AM source.
        """
        self._write('AM:SOUR {0}'.format(val))
        self.check_error()

    # TODO(Jeffrey): 'GND' or 'GRO'?
    def get_AM_coupling(self):
        """Returns the source coupling for AM.

        *RST value is DC.

        Returns:
          - str: source coupling for AM ('GRO', 'DC', 'AC').
        """
        val = self._read('AM:COUP?')
        self.check_error()
        return val

    def set_AM_coupling(self, val):
        """Sets the source coupling for AM. 'GROund' coupling is equivalent to
        having NONE displayed on the front panel; it does not turn AM off, but
        all sources are disconnected.

        Parameters:
          - val (str): source coupling for AM ('GRO', 'DC', 'AC').
        """
        self._write('AM:COUP {0}'.format(val))
        self.check_error()

    def get_AM_freq(self):
        """Returns the AM frequency in Hz.

        *RST value is 1 kHz.

        Alias to `get_LFS_freq`.

        Returns:
          - float: AM frequency .
        """
        val = self._read('AM:FREQ?')
        self.check_error()
        return val

    def set_AM_freq(self, val, unit='HZ'):
        """Sets the AM frequency.

        Alias to `set_LFS_freq`.

        Parameters:
          - val (float): AM frequency.
          - unit (str): Frequency unit.
        """
        self._write('AM:FREQ {0}'.format(val))
        self.check_error()

    def get_AM_freq_step(self):
        """Returns the AM frequency step size.

        *RST value is 100 Hz.

        Alias to `get_LFS_freq_step`.

        Returns:
          - float: AM frequency step size.
        """
        val = self._read('AM:FREQ:STEP:INCR?')
        self.check_error()
        return val

    def set_AM_freq_step(self, val):
        """Sets the AM frequency step size. 
        
        Alias to `set_LFS_freq_step`.

        Parameters:
          - val (float/str): AM frequency step size.
        """
        self._write('AM:FREQ:STEP:INCR {0}'.format(val))
        self.check_error()


    #########################
    ## Amplitude Subsystem ##
    #########################

    def get_amp_source_level(self):
        """Returns the CW amplitude.

        *RST value is -140.0 dBm.

        Returns:
          - float: CW amplitude.
        """
        val = self._read('AMPL:SOUR:LEV?')
        self.check_error()
        return val

    def set_amp_source_level(self, val):
        """Sets the CW amplitude.

        Parameters:
          - val (float/str): CW amplitude.
        """
        self._write('AMPL:SOUR:LEV {0}'.format(val))
        self.check_error()

    def get_amp_source_step(self):
        """Returns the amplitude step size.

        *RST value is 10 dB.

        Returns:
          - float: amplitude step size.
        """
        val = self._read('AMPL:SOUR:LEV:STEP:INCR?')
        self.check_error()
        return val

    def set_amp_source_step(self, val, unit=''):
        """Sets the amplitude step size.

        Parameters:
          - val (float/str): amplitude step size.
          - unit (str): Amplitude unit.
        """
        if unit:
            val = '{0} {1}'.format(val, unit)
        self._write('AMPL:SOUR:LEV:STEP:INCR {0}'.format(val))
        self.check_error()

    def get_amp_source_unit(self):
        """Returns the unit for amplitude steps.

        *RST value is dB.

        Returns:
          - str: Amplitude step unit.
        """
        val = self._read('AMPLITUDE:SOUR:LEV:UNIT?')
        self.check_error()
        return val

    def set_amp_source_unit(self, val):
        """Sets the unit for amplitude steps.

        Parameters:
          - val (str): Amplitude step unit.
        """
        self._write('AMPLITUDE:SOUR:LEV:UNIT {0}'.format(val))
        self.check_error()

    def get_amp_source_state(self):
        """Returns the state of the RF output. 'OFF' (0) indicates that the
        output is disabled, while 'ON' (1) indicates that it is enabled.
        Setting the amplitude source level does not turn this on implicitly.

        *RST value is 'OFF'.

        Returns:
          - float: Amplitude state.
        """
        val = self._read('AMPL:STAT?')
        self.check_error()
        return val

    def set_amp_source_state(self, val):
        """Sets the state of the RF output. 'OFF' (0) indicates that the output
        is disabled, while 'ON' (1) indicates that it is enabled. Setting the
        amplitude source level does not turn this on implicitly.

        Parameters:
          - val (float/str): Amplitude state.
        """
        self._write('AMPL:STAT {0}'.format(val))
        self.check_error()

    def get_funcname1(self):
        """Returns the description3

        *RST value is rstval4.

        Returns:
          - float: value2.
        """
        val = self._read('cmd0?')
        self.check_error()
        return val

    def set_funcname1(self, val):
        """Sets the description3

        Parameters:
          - val (float/str): value2.
        """
        self._write('cmd0 {0}'.format(val))
        self.check_error()


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
        raise InstrumentError("Error reading '{0}' from HP8664A: {1}".format(
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
        raise InstrumentError("Error writing '{0}' to HP8664A: {1}".format(
                val, instrument.get_error_msg()))

