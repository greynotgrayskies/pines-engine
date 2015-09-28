import visa
from instrument.base import *

# TODO(Jeffrey): Make sure definition is general.
class VisaInstrument(Instrument):
    _parameters = {}
    _instructions = {}

    def _connect(self):
        self._instr = visa.ResourceManager().open_resource(self.address)
        self._connected = True

    def _disconnect(self):
        self._instr.close()
        self._connected = False
        self._instr = None

    def _read(self, string):
        # TODO(Jeffrey): I doubt this is the only kind of error that might be
        # raised. Read should probably check for errors as well.
        try:
            return str(self._instr.query(string)).strip()
        except visa.VisaIOError as e:
            raise InstrumentError('Error reading command ({0}): {1}'.format(string, e.message))

    def _write(self, string):
        self._instr.write(string)
        # TODO(Jeffrey): This line is specific for HP8664A. Different
        # instruments may have different protocols for checking for errors.
        # Generalize? Or should we completely ignore erroneous writes?
        # To keep it general, it might be best to ignore errors. Instruments
        # can check for errors by themselves.
        error = self._read(self._instruction_str('check_error'))
        error, msg = error.strip().split(',')
        if error != '0':
            raise InstrumentError('Command ({0}) raised an error: {1} (Error code: {2})'.format(string, msg, error))
