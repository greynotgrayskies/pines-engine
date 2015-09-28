"""
PulseBlaster Module

The PulseBlaster module, which contains the PulseBlaster object interface and
setup.

Note that the `PULSEBLASTER_LIB_PATH` setting must be defined before this
module can be used.

Importable:
  - PulseBlaster
"""

from instrument.base import *
from instrument.lib.cinstrument import CInstrument
from settings import PULSEBLASTER_LIB_PATH as libpath

from ctypes import *

__all__ = ['PulseBlaster']

class PulseBlaster(CInstrument):
    """PulseBlaster interface.

    The PulseBlaster object interface, which needs a better docstring.

    PulseBlaster functions and documentation are adapted from SpinCore API:
    http://www.spincore.com/support/spinapi/reference/production/2013-09-25/spinapi_8h.html

    Parameters:
      - clock_freq (float): 
      - device_num (int):
      - program (list[PBInstruction]):
      ...

    Instance Attributes:
      - clock_freq (float):
      - device_num (int):
      - program (list[int]):
      ...

    Class Attributes:
      - opcodes (dict[str -> int]): 
      - devices (dict[str -> int]):
      - pulses (dict[str -> int]):
      ...
    """

    def __init__(self, clock_freq, device_num, program, **kwargs):
        CInstrument.__init__(self, **kwargs)
        self.clock_freq = clock_freq
        self.device_num = device_num
        self.program = program

    opcodes = {
        'CONTINUE':     0,
        'STOP':         1,
        'LOOP':         2,
        'END_LOOP':     3,
        'JSR':          4,
        'RTS':          5,
        'BRANCH':       6,
        'LONG_DELAY':   7,
        'WAIT':         8,
    }

    devices = {}

    pulses = {
        'OFF':          0 << 21,
        'ONE_PERIOD':   1 << 21,
        'TWO_PERIOD':   2 << 21,
        'THREE_PERIOD': 3 << 21,
        'FOUR_PERIOD':  4 << 21,
        'FIVE_PERIOD':  5 << 21,
        'ON':           7 << 21,
    }

    # SpinCore API functions, adapted for Python.

    @staticmethod
    def pb_count_boards():
        """Return the number of SpinCore boards present in your system.

        Returns:
            int: Number of boards present. -1 returned on error.
        """
        return PulseBlaster._lib.pb_count_boards()

    @staticmethod
    def pb_select_board(board):
        """If multiple boards from SpinCore Technologies are present in your
        system, this function allows you to select which board to talk to.  Once
        this function is called, all subsequent commands (such as pb_init(),
        pb_core_clock(), etc.) will be sent to the selected board.  You may
        change which board is selected at anytime.

        If you have only one board, it is not necessary to call this function.

        Parameters:
          - board (int): Species which board.  Counting starts at 0.

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_select_board(board)

    @staticmethod
    def pb_init():
        """Initializes the board. This must be called before any other
        functions are used which communicate with the board. If you have
        multiple boards installed in your system, `pb_select_board()` may be
        called first to select which board to initialize.

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_init()

    @staticmethod
    def pb_core_clock(clock_freq):
        """Tell the library which clock frequency the board uses. This should
        be called at the beginning of each program, right after you initialize
        the board with `pb_init()`. Note that this does not actually set the
        clock frequency, it simply tells the driver what frequency the board is
        using, since this cannot (currently) be autodetected.

        Also note that this frequency refers to the speed at which the
        PulseBlaster core itself runs. On many boards, this is different than
        the value printed on the oscillator. On RadioProcessor devices, the A/D
        converter and the PulseBlaster core operate at the same clock
        frequency.

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_core_clock(clock_freq)

    @staticmethod
    def pb_close():
        """End communication with the board. This is generally called as the
        last line in the program. Once this is called, no further communication
        can take place with the board unless the board is reinitialized with
        `pb_init()`. However, any pulse program that is loaded and running at
        the time of calling this function will continue to run indefinitely.

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_close()

    @staticmethod
    def pb_start_programming(device):
        """This function tells the board to start programming one of the
        onboard devices. Only one device can be programmed at a time.

        Parameters:
          - device (int): Specifies which device to start programming.

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_start_programming(device)

    @staticmethod
    def pb_stop_programming():
        """Finishes programming for a specific onboard device which was started
        by `pb_start_programming()`.

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_stop_programming()

    @staticmethod
    def pb_start():
        """Send a software trigger to the board. THis will start execution of a
        pulse program. It will also trigger a program which is currently paused
        due to a WAIT instruction. Triggering can also be accomplished throguh
        hardware, please see your board's manual for details on how to
        accomplish this.

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_start()

    @staticmethod
    def pb_stop():
        """Stops output of board. Analog output will return to ground, and TTL
        outputs will etiehr remain in the same state they were in when the
        reset command was received or return to ground. This also resets the
        PulseBlaster so that the PulseBlaster Core can be run again using
        `pb_start()` or a hardware trigger.

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_stop()

    @staticmethod
    def pb_reset():
        """Stops the output of board and resets the PulseBlaster Core. Analog
        output will return to ground, and TTL outputs will either remain in the
        same state they were in when the reset command was receivd or return to
        ground. This also resets the PulseBlaster Core so that the board can be
        run again using `pb_start()` or a hardware trigger. Note: Either
        `pb_reset()` or `pb_stop()` must be called before `pb_start()` if the
        pulse program is to be run from the beginning (as opposed to continuing
        from a WAIT state).

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_reset()

    @staticmethod
    def pb_inst_pbonly(flags, inst, inst_data, length):
        """This is the instruction programming function for boards without a
        DDS. (for example PulseBlaster and PulseBlasterESR boards). Syntax is
        identical to that of `pb_inst_tworf()`, except that the parameters
        pertaining to the analog outputs are not used.
        
        Parameters:
          - flags (int): Set every bit to one for each flag you want to set
            high.
          - inst (int): Specify the instruction you want.
          - inst_data (int): Instruction specific data.
          - length (double): Length of this instruction in nanoseconds.

        Returns:
          - int: 0 on success, a negative number on failure.
        """
        return PulseBlaster._lib.pb_inst_pbonly(
                c_uint(flags),
                c_int(inst),
                c_int(inst_data),
                c_double(length),
        )

    @staticmethod
    def pb_get_error():
        """Return the most recent error string. Anytime a function (such as
        `pb_init()`, `pb_start_programming()`, etc.) encounters an error, this
        function will return a description of what went wrong.

        Returns:
          - str: A string describing the last error returned. A string
            contaning "No Error" is returned if the last function call was
            successful.
        """
        return PulseBlaster._lib.pb_get_error().decode('utf-8')

_FUNCTIONS = {
    'pb_count_boards':          (c_int, ()),
    'pb_select_board':          (c_int, (c_int,)),
    'pb_init':                  (c_int, ()),
    'pb_core_clock':            (None, (c_double,)),
    'pb_close':                 (c_int, ()),
    'pb_start_programming':     (c_int, (c_int,)),
    'pb_stop_programming':      (c_int, ()),
    'pb_start':                 (c_int, ()),
    'pb_stop':                  (c_int, ()),
    'pb_reset':                 (c_int, ()),
    'pb_inst_pbonly':           (c_int, (c_longlong,)),
    'pb_get_error':             (c_char_p, ()),
}

PulseBlaster.loadDLL(libpath, _FUNCTIONS)

class PBInstruction(object):
    """PulseBlasterESR-PRO instruction.

    Parameters:
        flags (int):
        inst (str): Flow control command.
        inst_data (int): Instruction specific data.
        length (float): Duration of this instruction in nanoseconds.
        address (int): Address of this instruction (initialized as None)
    """

    def __init__(self, flags, inst, inst_data, length):
        self.flags = flags
        self.inst = inst
        self.inst_data = inst_data
        self.length = length
        self.address = None

    def write_instruction(self):
        self.address = PulseBlasterESRPRO.pb_inst_pbonly(
                self.flags,
                self.opcode[self.inst],
                self.inst_data,
                self.length,
        )

class PBContinueInst(PBInstruction):
    def __init__(self, flags, length):
        PBInstruction.__init__(self, flags, 'CONTINUE', 0, length)

class PBStopInst(PBInstruction):
    def __init__(self, flags, length):
        PBInstruction.__init__(self, flags, 'STOP', 0, length)

class PBLoopInst(PBInstruction):
    def __init__(self, flags, length, num_loops):
        PBInstruction.__init__(self, flags, 'LOOP', num_loops, length)

class PBEndLoopInst(PBInstruction):
    def __init__(self, flags, length, loop_inst):
        PBInstruction.__init__(self, flags, 'ENDLOOP', loop_inst, length)

