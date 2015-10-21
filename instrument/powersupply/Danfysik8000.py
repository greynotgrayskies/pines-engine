from instrument import *
from instrument.powersupply import *
from instrument.lib.visainstrument import *
import visa

class Danfysik8000(PowerSupply, VisaInstrument):
    def _reset(self):
        # Investigate Danfysik reset parameters - see short list. 
        self._write('REM')        
        """Change to remote control
        """
        self._write('PO +')
        """Set to normal polarity
        """
        self._write('N')
        """Turn power supply off"""
        
    def get_error_msg(self):
        """Returns texted error message 
        """
        val=self._read('ERRT')
        self.check_error()
        return val

    ##########################
    ## Danfysik 8000 Commands ##
    #########################
    

    def set_on(self):
        """Turns power supply on
        """
        self._write('N')
        self.check_error()
        
    def set_off(self):
        """Turns power supply off
        """
        self._write('F')
        self.check_error()
    
    def set_current(self, val):
        """Sets output current in percent. e.g. WA 900000 gives 90% of total
        possible current
        """
        self._write('WA {0}'.format(val))
        self.check_error()

    def get_current(self):
        """Returns the total current in percent.
        Returns:
          - float: "DDDDDD", where D is number from 0 to 9. 
        """
        val = self._read('RA')
        self.check_error()
        return val
        
    def get_values(self, val):
        """Function: Reads values from the scanning 8-bit ADC and the
                    optional 16-bid ADC.
            Syntax: 'AD X' Where X is a  number from 0 to 9
            Details: 0:current, 1:Tesla, 2:Voltage, 3: Internal +15V
                     4: Internal -15V, 5: Internal +5V, 6: Delta temperature
                     7: Trans.bank Vce (Volts), 8: Option Iout (16-bit)
                     9: Aux. Iout (cont. panel). For more info see 
                     Danfysik 8000 IEEE 488 Programming"""        
        val = self._read('AD {0}'.format(val))
        self.check_error()
        return val
        
    def get_control_mode(self):
        """Causes the MPS to respond with its current control mode. 
        Syntax: 'CMD'
        Will respond with one of the following text-strings:
        'REM' : REMote control.
        'LOC' : LOCal control, i. e. cotrolled via the control panel."""
        val = self._read('CMD')
        self.check_error()
        return val
        
    def set_clear_byte(self, val):
        """Clears bits in the status byte but cannot access all bits
        Syntax: 'CS XXX' , Where X is a number from 0 to 9, 
                and range is from  0 to 255
        Details: Content of status byte can be intepreted using Danfysik 8000 
                IEEE 488 Programiing manual"""
        val = self._write('CS {0}'.format(val))
        self.check_error()
        return val
        
    def set_local(self):
        """Function: Will change the control mode of the MPS to LOCal control
           """
        self._write('LOC')
        self.check_error()
        
    def set_remote(self):
        """Function: Will change the control mode of the MPS to REMote control
           """
        self._write('REM')
        self.check_error()
        
    def set_lock(self):
        """Function: This command is used to lock the MPS in LOCal control mode
           """
        self._write('LOCK')
        self.check_error()
        
    def set_unlock(self):
        """Function: This command is used to unlock the MPS in LOCal control mode
           whereafter the remote device can change the control mode freely"""
        self._write('UNLOCK')
        self.check_error()
        
         
    def get_polarity(self):
        """Function: Read the present polarity status of the MPS
            Details: The response can either be:
                    '+' Indicating Normal polarity.
                    Or
                    '-' Indicating Reverse polarity
                    If the MPS is not provided with a polarity reversal switch
                    the response will be '+'
                    """
        val = self._read('PO')
        self.check_error()
        return val
        
    def set_polarity(self, val):
        """Function: If the MPS is provided with a polarity reversal switch,
            these commands are used to change the polarity on the output of 
            the Power Supply"""
        self._write('PO {0}'.format(val))
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
        raise InstrumentError("Error reading '{0}' from Danfysik8000: {1}".format(
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
        raise InstrumentError("Error writing '{0}' to Danfysik8000: {1}".format(
                val, instrument.get_error_msg()))