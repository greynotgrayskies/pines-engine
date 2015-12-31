"""
HP8664A Module

HP8664A Module, which contains the HP8664A class.

Documentation for the HP8664A can be found here:
http://literature.cdn.keysight.com/litweb/pdf/08665-90078.pdf?id=88769

Importable:
  - HP8664A
"""
from instrument import *
from instrument.mwfreqsynth import *
from instrument.lib.visainstrument import *
import visa

__all__ = ['HP8664A']

class HP8664A(MWFreqSynth, VisaInstrument):
    """HP8664A Instrument Class.

    Parameters:
      ...

    Instance Attributes:
      ...

    Class Attributes:
      ...
    """

    #######################
    ## Overriden Methods ##
    #######################

    def _reset(self):
        set_presets_inst(self)

    def get_power(self):
        return self.get_amp_inst()

    def set_power(self, power, unit=''):
        self.set_amp_inst(power, unit)

    def get_freq(self):
        return self.get_freq_inst()

    def set_freq(self, freq, unit=''):
        self.set_freq_inst(freq, unit)

    def _get_error_no(self):
        return int(self.get_error_inst())

    def _get_error_msg(self):
        return self.get_error_inst('STR').split(',')[1].strip()

    #####################
    ## HP8664A Methods ##
    #####################

    # Methods here are unique to the HP8664A class. There's no need to make
    # them private, but calling them from an experiment means that the
    # experiment will be dependent on a particular instrument.

    #####################
    ## System Commands ##
    #####################

    def set_presets_inst(self):
        """Causes the Signal Generator to do an instrument preset, and sets all
        operating parameters to their *RST value.
        """
        self._write('*RST')

    def get_error_inst(self, error_format='NUM'):
        """Reads an error from the system error queue. Returns a zero if the
        queue is empty. If a numeric format is used, the signal generator
        returns only a number. If a string format is used, then the signal
        generator returns a number followed by a comma, and a quoted string
        containing a standard generic error message, a colon, and a specific
        error message.

        Parameters:
          - error_format (str): An error format ('NUM' or 'STR')

        Returns:
          - str: Error output
        """
        return self._read('SYST:ERR? {0}'.format(error_format))

    ##################
    ## AM Subsystem ##
    ##################

    @VisaInstrument.check_error
    def get_am_depth_inst(self):
        """Gets the AM depth in percent.

        *RST value is 0%.

        Returns:
          - float: AM depth in percent.
        """
        return self._read('AM:DEPTH?')

    @VisaInstrument.check_error
    def set_am_depth_inst(self, val):
        """Sets the AM depth in percent.

        Can also set the AM depth to the 'MIN' or 'MAX' AM depth.
        
        Parameters:
         - val (float/str): AM depth in percent.
        """
        self._write('AM:DEPTH {0}'.format(val))

    @VisaInstrument.check_error
    def get_am_depth_step_inst(self):
        """Returns the AM depth step size in percent.

        *RST value is 1%.

        Returns:
          - float: AM depth step size in percent.
        """
        return self._read('AM:DEPTH:STEP:INCR?')

    @VisaInstrument.check_error
    def set_am_depth_step_inst(self, val):
        """Sets the AM depth size in percent.

        Can also set the AM depth step size to the 'MIN' or 'MAX' AM depth step
        size.

        Parameters:
          - val (float/str): AM depth step size in percent.
        """
        self._write('AM:DEPTH:STEP:INCR {0}'.format(val))

    @VisaInstrument.check_error
    def get_AM_state_inst(self):
        """Returns the AM modulation state, which is either 'ON' (1) or 'OFF'
        (0).

        *RST value is 'OFF'.

        Returns:
          - float: AM modulation state.
        """
        return self._read('AM:STAT?')

    @VisaInstrument.check_error
    def set_AM_state_inst(self, val):
        """Sets the AM modulation state, which is either 'ON' (1) or 'OFF' (0).

        Parameters:
          - val (float/str): AM modulation state.
        """
        self._write('AM:STAT {0}'.format(val))

    @VisaInstrument.check_error
    def get_AM_source_inst(self):
        """Returns the AM source.

        *RST value is 'INT'.

        Returns:
          - str: AM source.
        """
        return self._read('AM:SOUR?')

    @VisaInstrument.check_error
    def set_AM_source_inst(self, val):
        """Sets the AM source: 'EXTernal' or 'INTernal'. 'INTernal,EXTernal' is
        accepted but will cause an execution error since the Signal Generator
        does not use both the internal audio source and an external audio
        source at the same time..

        Parameters:
          - val (str): AM source.
        """
        self._write('AM:SOUR {0}'.format(val))

    @VisaInstrument.check_error
    def get_AM_coupling_inst(self):
        """Returns the source coupling for AM.

        *RST value is DC.

        Returns:
          - str: source coupling for AM ('GRO', 'DC', 'AC').
        """
        return self._read('AM:COUP?')

    @VisaInstrument.check_error
    def set_AM_coupling_inst(self, val):
        """Sets the source coupling for AM. 'GROund' coupling is equivalent to
        having NONE displayed on the front panel; it does not turn AM off, but
        all sources are disconnected.

        Parameters:
          - val (str): source coupling for AM ('GRO', 'DC', 'AC').
        """
        self._write('AM:COUP {0}'.format(val))

    @VisaInstrument.check_error
    def get_AM_freq_inst(self):
        """Returns the AM frequency in Hz.

        *RST value is 1 kHz.

        Alias to `get_LFS_freq`.

        Returns:
          - float: AM frequency .
        """
        return self._read('AM:FREQ?')

    @VisaInstrument.check_error
    def set_AM_freq_inst(self, val, unit='HZ'):
        """Sets the AM frequency.

        Alias to `set_LFS_freq`.

        Parameters:
          - val (float): AM frequency.
          - unit (str): Frequency unit.
        """
        self._write('AM:FREQ {0}'.format(val))

    @VisaInstrument.check_error
    def get_AM_freq_step_inst(self):
        """Returns the AM frequency step size.

        *RST value is 100 Hz.

        Alias to `get_LFS_freq_step`.

        Returns:
          - float: AM frequency step size.
        """
        return self._read('AM:FREQ:STEP:INCR?')

    @VisaInstrument.check_error
    def set_AM_freq_step_inst(self, val):
        """Sets the AM frequency step size. 
        
        Alias to `set_LFS_freq_step`.

        Parameters:
          - val (float/str): AM frequency step size.
        """
        self._write('AM:FREQ:STEP:INCR {0}'.format(val))


    #########################
    ## Amplitude Subsystem ##
    #########################

    @VisaInstrument.check_error
    def get_amp_inst(self):
        """Returns the CW amplitude.

        *RST value is -140.0 dBm.

        Returns:
          - float: CW amplitude.
        """
        return self._read('AMPL:SOUR:LEV?')

    @VisaInstrument.check_error
    def set_amp_inst(self, val):
        """Sets the CW amplitude.

        Parameters:
          - val (float/str): CW amplitude.
        """
        self._write('AMPL:SOUR:LEV {0}'.format(val))

    @VisaInstrument.check_error
    def get_amp_source_level_inst(self):
        """Returns the CW source amplitude.

        *RST value is -140.0 dBm.

        Returns:
          - float: CW amplitude.
        """
        return self._read('AMPL:SOUR:LEV?')

    @VisaInstrument.check_error
    def set_amp_source_level_inst(self, val):
        """Sets the CW source amplitude.

        Parameters:
          - val (float/str): CW amplitude.
        """
        self._write('AMPL:SOUR:LEV {0}'.format(val))

    @VisaInstrument.check_error
    def get_amp_source_step_inst(self):
        """Returns the source amplitude step size.

        *RST value is 10 dB.

        Returns:
          - float: amplitude step size.
        """
        return self._read('AMPL:SOUR:LEV:STEP:INCR?')

    @VisaInstrument.check_error
    def set_amp_source_step_inst(self, val, unit=''):
        """Sets the source amplitude step size.

        Parameters:
          - val (float/str): amplitude step size.
          - unit (str): Amplitude unit.
        """
        if unit:
            return '{0} {1}'.format(val, unit)
        self._write('AMPL:SOUR:LEV:STEP:INCR {0}'.format(val))

    @VisaInstrument.check_error
    def get_amp_source_unit_inst(self):
        """Returns the unit for source amplitude steps.

        *RST value is dB.

        Returns:
          - str: Amplitude step unit.
        """
        return self._read('AMPLITUDE:SOUR:LEV:UNIT?')

    @VisaInstrument.check_error
    def set_amp_source_unit_inst(self, val):
        """Sets the unit for source amplitude steps.

        Parameters:
          - val (str): Amplitude step unit.
        """
        self._write('AMPLITUDE:SOUR:LEV:UNIT {0}'.format(val))

    @VisaInstrument.check_error
    def get_amp_source_state_inst(self):
        """Returns the state of the RF source output. 'OFF' (0) indicates that
        the output is disabled, while 'ON' (1) indicates that it is enabled.
        Setting the amplitude source level does not turn this on implicitly.

        *RST value is 'OFF'.

        Returns:
          - float: Amplitude state.
        """
        return self._read('AMPL:STAT?')

    @VisaInstrument.check_error
    def set_amp_source_state_inst(self, val):
        """Sets the state of the RF source output. 'OFF' (0) indicates that the
        output is disabled, while 'ON' (1) indicates that it is enabled.
        Setting the amplitude source level does not turn this on implicitly.

        Parameters:
          - val (float/str): Amplitude state.
        """
        self._write('AMPL:STAT {0}'.format(val))

    #########################
    ## Frequency Subsystem ##
    #########################

    @VisaInstrument.check_error
    def get_freq_inst(self):
        """Returns the non-swept frequency. Does not disable sweep.

        *RST value is 1500 MHz.

        Returns:
          - float: Non-swept frequency.
        """
        return self._read('FREQ?')

    @VisaInstrument.check_error
    def set_freq_inst(self, freq, unit=''):
        """Sets the non-swept frequency. Does not disable sweep.

        *RST value is 1500 MHz.

        Parameters:
          - freq (float): Non-swept frequency.
          - unit (str): Frequency unit ('HZ', 'KHZ', 'MHZ', 'MAHZ', 'GHZ').
        """
        if unit != '':
            unit = ' ' + unit
        return self._read('FREQ {0}{1}'.format(freq, unit))

