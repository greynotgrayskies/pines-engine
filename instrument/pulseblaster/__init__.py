"""
PulseBlaster Module

The PulseBlaster module, which contains the PulseBlaster object interface and
setup.

Note that the `PULSEBLASTER_LIB_PATH` setting must be defined before this
module can be used.

Importable:
  - PulseBlaster
"""

from instrument import *
from instrument.lib.cinstrument import CInstrument
from settings import PULSEBLASTER_LIB_PATH as libpath

from ctypes import *

__all__ = ['PulseBlaster']

class PulseBlaster(CInstrument):
    """PulseBlaster interface.

    The PulseBlaster object interface, which loads the SpinCore library and
    wraps the C methods to be more Python-like.

    Some PulseBlaster models have different instruction formats, so each model
    should have its own instruction writing functions (e.g. `continue_inst`,
    `stop_inst`).

    PulseBlaster functions and documentation are adapted from SpinCore API:
    http://www.spincore.com/support/spinapi/reference/production/2013-09-25/spinapi_8h.html

    Parameters:
      - clock_freq (float):
      - device_num (int):
      ...

    Instance Attributes:
      - clock_freq (float):
      - board_num (int):
      ...

    Class Attributes:
      - opcodes (dict[str -> int]):
      - devices (dict[str -> int]):
      - pulses (dict[str -> int]):
      ...
    """

    def __init__(self, clock_freq, board_num, **kwargs):
        CInstrument.__init__(self, **kwargs)
        self.clock_freq = clock_freq
        self.board_num = board_num

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

    devices = {
        'PULSE_PROGRAM':    0,
        'FREQ_REGS':        1,
        'PHASE_REGS':       2,
        'TX_PHASE_REGS':    2,
        'PHASE_REGS_1':     2,
        'RX_PHASE_REGS':    3,
        'PHASE_REGS_0':     3,
        'COS_PHASE_REGS':   51,
        'SIN_PHASE_REGS':   50,
    }

    pulses = {
        'OFF':          0 << 21,
        'ONE_PERIOD':   1 << 21,
        'TWO_PERIOD':   2 << 21,
        'THREE_PERIOD': 3 << 21,
        'FOUR_PERIOD':  4 << 21,
        'FIVE_PERIOD':  5 << 21,
        'ON':           7 << 21,
    }

    #######################
    ## Overriden Methods ##
    #######################

    def _connect(self):
        self.initialize()

    # TODO(Jeffrey): Check to see if board properly disconnects if in the
    # middle of writing a PulseBlaster program.
    def _disconnect(self):
        self.stop()
        self.close()

    def _reset(self):
        self.reset()


    ##########################
    ## PulseBlaster Methods ##
    ##########################

    @staticmethod
    def count_boards():
        """Return the number of SpinCore boards present.

        Returns:
            int: Number of boards present.
        """
        num_boards = pb_count_boards()
        if num_boards < 0:
            raise InstrumentError(pb_get_error())
        return num_boards

    def select_board(self):
        """If multiple SpinCore Technologies boards are present, selects this
        board to communicate with. All subsequent PulseBlaster commands will be
        sent to this board.
        """
        if pb_select_board(self.board_num) < 0:
            raise InstrumentError(pb_get_error())

    def initialize(self):
        """Initializes the board. Must be called when connecting to a
        PulseBlaster instrument.

        Combines the `pb_init` and `pb_core_clock` functions, since they should
        be called together anyways.

        Note: Should only be called by the `_connect method`.
        """
        self.select_board()
        if pb_init() < 0:
            raise InstrumentError(pb_get_error())
        pb_core_clock(self.clock_freq)

    def close(self):
        """End communication with the board. Once called, no further
        communication can take place with the board unless the board is
        reinitialized. However, any pulse program that is loaded and running at
        the time of calling this function will continue to run indefinitely.

        Note: Should only be called by the `_disconnect` method.
        """
        self.select_board()
        if pb_close() < 0:
            raise InstrumentError(pb_get_error())

    def start_programming(self, device):
        """Starts programming one of the onboard devices. Only one device may
        be programmed at a time.

        Parameters:
          - device (str): a device, as specified by `PulseBlaster.devices`
        """
        self.select_board()
        if device not in PulseBlaster.devices:
            raise InstrumentError(
                    "Invalid PulseBlaster programming target: '{0}'".format(
                            device))
        if pb_start_programming(PulseBlaster.devices[device]) < 0:
            raise InstrumentError(self.get_error())

    def stop_programming(self):
        """Finishes programming for a specific onboard device which was started by
        `start_programming`.
        """
        if pb_stop_programming() < 0:
            raise InstrumentError(self.get_error())
    
    def start(self):
        """Send a software trigger to the board to start execution of a pulse
        program. It will also trigger a program which is currently paused due
        to a WAIT instruction.
        """
        self.select_board()
        if pb_start() < 0:
            raise InstrumentError(self.get_error())

    def stop(self):
        """Stops output of board. Analog output will return to ground, and TTL
        outputs will either remain in the same state they were in when the
        reset command was received or return to ground. 

        Also resets the PulseBlaster so that the PulseBlaster Core can be run
        again using `start` or a hardware trigger.
        """
        self.select_board()
        if pb_stop() < 0:
            raise InstrumentError(self.get_error())

    def reset(self):
        """Stops output of board and resets the PulseBlaster Core. Analog
        output will return to ground, and TTL outputs will remain eithre in the
        same state they were in when the reset command was receieved or return
        to ground.

        Either `stop` or `reset` must be called before `start` if the pulse
        program is to be run from the beginning (as opposed to continuing from
        a WAIT state.
        """
        self.select_board()
        if pb_reset() < 0:
            raise InstrumentError(self.get_error())

    ######################
    ## Abstract Methods ##
    ######################

    # Notes from SpinCore manual:
    #  -[1] For instructions longer than 8589 ms, please use a LONG_DELAY
    #       instruction.
    #  -[2] For PulseBlasterESR-PRO-500 design 17-11, instructions with
    #       CONTINUE, JSR, RTS and LONG_DELAY opcodes require a minimum
    #       instruction length of at least 6 clock-cycles (12 ns).

    @staticmethod
    def continue_inst(flags, pulse, length):
        """Sends a CONTINUE instruction to a PulseBlaster. Program execution
        continues to next instruction. See note [1] and [2].

        Assumes that `pb_start_programming()` has been called first.

        Parameters:
          - flags (int): Bit field specifying which flags are set to high.
          - pulse (str): A pulse period, as specified by the `pulses`
            dictionary.
          - length (float): Length of the instruction in nanoseconds.

        Returns:
          - int: Address of the created instruction.
        """
        return NotImplemented

    @staticmethod
    def stop_inst(flags, pulse, length):
        """Sends a STOP instruction to a PulseBlaster. Stop execution of
        program. Aborts the operation of the micro-controller with no control
        of output states (all TTL values remain from previous instruction).
        Recommended thatprior to the STOP opcode, a shot interval (minimum six
        clock cycles) be added to set the output states as desired.

        Assumes that `pb_start_programming()` has been called first.

        Parameters:
          - flags (int): Bit field specifying which flags are set to high.
          - pulse (str): A pulse period, as specified by the `pulses`
            dictionary.
          - length (float): Length of the instruction in nanoseconds.

        Returns:
          - int: Address of the created instruction.
        """
        return NotImplemented

    @staticmethod
    def loop_inst(flags, pulse, length, num_loops):
        """Sends a LOOP instruction to a PulseBlaster. Specify beginning of a
        loop. Execution continues to next instruction. Data used to specify
        number of loops.

        Assumes that `pb_start_programming()` has been called first.

        Parameters:
          - flags (int): Bit field specifying which flags are set to high.
          - pulse (str): A pulse period, as specified by the `pulses`
            dictionary.
          - length (float): Length of the instruction in nanoseconds.
          - num_loops (int): Number of loops.

        Returns:
          - int: Address of the created instruction.
        """
        return NotImplemented

    @staticmethod
    def end_loop_inst(flags, pulse, length, addr):
        """Sends a END_LOOP instruction to a PulseBlaster. Specify the end of a
        loop. Execution returns to beginning of loop and decrements loop
        counter.

        Assumes that `pb_start_programming()` has been called first.

        Parameters:
          - flags (int): Bit field specifying which flags are set to high.
          - pulse (str): A pulse period, as specified by the `pulses`
            dictionary.
          - length (float): Length of the instruction in nanoseconds.
          - addr (int): The address of the beginning loop.

        Returns:
          - int: Address of the created instruction.
        """
        return NotImplemented

    @staticmethod
    def jsr_inst(flags, pulse, length, addr):
        """Sends a JSR instruction to a PulseBlaster. Program execution jumps
        to beginning of a subroutine. See note [2].

        Assumes that `pb_start_programming()` has been called first.

        Parameters:
          - flags (int): Bit field specifying which flags are set to high.
          - pulse (str): A pulse period, as specified by the `pulses`
            dictionary.
          - length (float): Length of the instruction in nanoseconds.
          - addr (int): The address of the first subroutine instruction.

        Returns:
          - int: Address of the created instruction.
        """
        return NotImplemented

    @staticmethod
    def rts_inst(flags, pulse, length):
        """Sends a RTS instruction to a PulseBlaster. Program execution returns
        to instruction after JSR was called. See note [2].

        Assumes that `pb_start_programming()` has been called first.

        Parameters:
          - flags (int): Bit field specifying which flags are set to high.
          - pulse (str): A pulse period, as specified by the `pulses`
            dictionary.
          - length (float): Length of the instruction in nanoseconds.

        Returns:
          - int: Address of the created instruction.
        """
        return NotImplemented

    @staticmethod
    def branch_inst(flags, pulse, length, addr):
        """Sends a BRANCH instruction to a PulseBlaster. Program execution
        continues at specified instruction.

        Assumes that `pb_start_programming()` has been called first.

        Parameters:
          - flags (int): Bit field specifying which flags are set to high.
          - pulse (str): A pulse period, as specified by the `pulses`
            dictionary.
          - length (float): Length of the instruction in nanoseconds.
          - addr (int): The address of the first subroutine instruction.

        Returns:
          - int: Address of the created instruction.
        """
        return NotImplemented

    @staticmethod
    def long_delay_inst(flags, pulse, length, delay):
        """Sends a LONG_DELAY instruction to a PulseBlaster. For long interval
        instructions. Data field specifies a multiplier of the delay field.
        Execution continues to next instuction. See note [2].

        Assumes that `pb_start_programming()` has been called first.

        Parameters:
          - flags (int): Bit field specifying which flags are set to high.
          - pulse (str): A pulse period, as specified by the `pulses`
            dictionary.
          - length (float): Length of the instruction in nanoseconds.
          - delay (int): Multiplier of the delay.

        Returns:
          - int: Address of the created instruction.
        """
        return NotImplemented

    @staticmethod
    def wait_inst(flags, pulse, length):
        """Sends a WAIT instruction to a PulseBlaster. Program execution stops
        and waits for a software or hardware trigger. Execution continues to
        next instruction after receipt of trigger. The latency is equal to the
        delay value entred in the WAIT instruction line, plus a fixed delay of
        6 clock cycles. The WAIT opcode may not be used by the first
        instruction in memory.

        Assumes that `pb_start_programming()` has been called first.

        Parameters:
          - flags (int): Bit field specifying which flags are set to high.
          - pulse (str): A pulse period, as specified by the `pulses`
            dictionary.
          - length (float): Length of the instruction in nanoseconds.

        Returns:
          - int: Address of the created instruction.
        """
        return NotImplemented


############################
## SpinCore API Functions ##
############################

# SpinCore API functions, adapted for Python. Should avoid calling directly
# outside from this class, unless it is needed explicitly.

def pb_count_boards():
    """Return the number of SpinCore boards present in your system.

    Returns:
        int: Number of boards present. -1 returned on error.
    """
    return PulseBlaster._lib.pb_count_boards()

def pb_select_board(board):
    """If multiple boards from SpinCore Technologies are present in your
    system, this function allows you to select which board to talk to.  Once
    this function is called, all subsequent commands (such as pb_init(),
    pb_core_clock(), etc.) will be sent to the selected board.  You may change
    which board is selected at anytime.

    If you have only one board, it is not necessary to call this function.

    Parameters:
      - board (int): Species which board.  Counting starts at 0.

    Returns:
      - int: 0 on success, a negative number on failure.
    """
    return PulseBlaster._lib.pb_select_board(board)

def pb_init():
    """Initializes the board. This must be called before any other functions
    are used which communicate with the board. If you have multiple boards
    installed in your system, `pb_select_board()` may be called first to select
    which board to initialize.

    Returns:
      - int: 0 on success, a negative number on failure.
    """
    return PulseBlaster._lib.pb_init()

def pb_core_clock(clock_freq):
    """Tell the library which clock frequency the board uses. This should be
    called at the beginning of each program, right after you initialize the
    board with `pb_init()`. Note that this does not actually set the clock
    frequency, it simply tells the driver what frequency the board is using,
    since this cannot (currently) be autodetected.

    Also note that this frequency refers to the speed at which the PulseBlaster
    core itself runs. On many boards, this is different than the value printed
    on the oscillator. On RadioProcessor devices, the A/D converter and the
    PulseBlaster core operate at the same clock frequency.

    Parameters:
      - clock_freq (float):
    """
    PulseBlaster._lib.pb_core_clock(clock_freq)

def pb_close():
    """End communication with the board. This is generally called as the last
    line in the program. Once this is called, no further communication can take
    place with the board unless the board is reinitialized with `pb_init()`.
    However, any pulse program that is loaded and running at the time of
    calling this function will continue to run indefinitely.

    Returns:
      - int: 0 on success, a negative number on failure.
    """
    return PulseBlaster._lib.pb_close()

def pb_start_programming(device):
    """This function tells the board to start programming one of the onboard
    devices. Only one device can be programmed at a time.

    Parameters:
      - device (int): Specifies which device to start programming.

    Returns:
      - int: 0 on success, a negative number on failure.
    """
    return PulseBlaster._lib.pb_start_programming(device)

def pb_stop_programming():
    """Finishes programming for a specific onboard device which was started by
    `pb_start_programming()`.

    Returns:
      - int: 0 on success, a negative number on failure.
    """
    return PulseBlaster._lib.pb_stop_programming()

def pb_start():
    """Send a software trigger to the board. THis will start execution of a
    pulse program. It will also trigger a program which is currently paused due
    to a WAIT instruction. Triggering can also be accomplished throguh
    hardware, please see your board's manual for details on how to accomplish
    this.

    Returns:
      - int: 0 on success, a negative number on failure.
    """
    return PulseBlaster._lib.pb_start()

def pb_stop():
    """Stops output of board. Analog output will return to ground, and TTL
    outputs will either remain in the same state they were in when the reset
    command was received or return to ground. This also resets the PulseBlaster
    so that the PulseBlaster Core can be run again using `pb_start()` or a
    hardware trigger.

    Returns:
      - int: 0 on success, a negative number on failure.
    """
    return PulseBlaster._lib.pb_stop()

def pb_reset():
    """Stops the output of board and resets the PulseBlaster Core. Analog
    output will return to ground, and TTL outputs will either remain in the
    same state they were in when the reset command was receivd or return to
    ground. This also resets the PulseBlaster Core so that the board can be run
    again using `pb_start()` or a hardware trigger. Note: Either `pb_reset()`
    or `pb_stop()` must be called before `pb_start()` if the pulse program is
    to be run from the beginning (as opposed to continuing from a WAIT state).

    Returns:
      - int: 0 on success, a negative number on failure.
    """
    return PulseBlaster._lib.pb_reset()

def pb_inst_pbonly(flags, inst, inst_data, length):
    """This is the instruction programming function for boards without a DDS.
    (for example PulseBlaster and PulseBlasterESR boards). Syntax is identical
    to that of `pb_inst_tworf()`, except that the parameters pertaining to the
    analog outputs are not used.

    Parameters:
      - flags (int): Set every bit to one for each flag you want to set
        high.
      - inst (int): Specify the instruction you want.
      - inst_data (int): Instruction specific data.
      - length (double): Length of this instruction in nanoseconds.

    Returns:
      - int: The address of the created instruction, or a negative number
        on failure.
    """
    return PulseBlaster._lib.pb_inst_pbonly(
            c_uint(flags),
            c_int(inst),
            c_int(inst_data),
            c_double(length),
    )

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
    'pb_inst_pbonly':           (c_int, (c_uint, c_int, c_int, c_double)),
    'pb_get_error':             (c_char_p, ()),
}

PulseBlaster.loadDLL(libpath, _FUNCTIONS)

