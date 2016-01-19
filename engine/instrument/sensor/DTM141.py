# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:53:06 2015

@author: Mirja

Things to ask about:
where does the instrument get it's address? Where is that indicator?
How will these commands show up on the user interface? _reset? get_error_no?
What do the user inputs look like?
"""

from instrument import *
from instrument.sensor import *
from instrument.lib.visainstrument import *
import visa

    ##########################
    ## DTM 141 Sensor Reset ##
    #########################


class DTM141(Sensor, VisaInstrument):

    def _reset(self):
        self._write('SDC')
        """SDC command does the following:
        a) normal field display selected
        b) 3 tesla range selected if 4 range teslameter
        c) peak hold value reset
        d) triggered mode cancelled
        e) GPIB I/O buffers cleared
        f) GPIB software reinitialized
        g) serial poll byte and SRQ cleared
        h) parallel port unconfigured
        """
        self._write('EO')
        """EO Erase offset - sets offset to 0 (all ranges)
        """
        self._write('EC')
        """EO Erase calibration - sets offset to 0 (all ranges)
        """
        self._write('GD')
        """General function DC - puts DTM in dc field measurement mode
        """
        self.check_error()
        
    def get_error_no(self):
        pass
    def get_error_msg(self):
        pass

    ############################################################
    ## DTM 141 Magnetic Field and Temperature Sensor Commands ##
    ############################################################

    def get_field(self):
        """Reads the sensor's measurement of magnetic field.
        Returns:
          - float: units in Tesla.
        """
        val = self._read('WE')
        self.check_error()
        return val

    def get_temperature(self):
        """Returns the sensor's measurement of temperature.
        Returns:
          - float: units in Celsius.
        """
        val = self._read('T')
        self.check_error()
        return val

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
        raise InstrumentError("Error reading '{0}' from DTM141: {1}".format(
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
        raise InstrumentError("Error writing '{0}' to DTN141: {1}".format(
                val, instrument.get_error_msg()))