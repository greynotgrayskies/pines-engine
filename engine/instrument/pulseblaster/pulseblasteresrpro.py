"""
PulseBlasterESR-PRO Module

The PulseBlasterESR-PRO module, which contains the PulseBlasterESRPRO object.

Importable:
  - PulseBlasterESRPRO
"""

from instrument import *
from instrument.pulseblaster import *
from ctypes import *

__all__ = ['PulseBlasterESRPRO']

FLAGS_SIZE = 21
INST_DATA_SIZE = 20
DELAY_COUNT_SIZE = 32

class PulseBlasterESRPRO(PulseBlaster):
    """PulseBlasterESR-PRO class.

    Parameters:
      ...

    Instance Attributes:
      ...

    Class Attributes:
      ...
    """

    ######################################
    ## PulseBlasterESR-PRO Instructions ##
    ######################################

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
        return _write_inst(flags, pulse, 'CONTINUE', 0, length)

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
        return _write_inst(flags, pulse, 'STOP', 0, length)

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
        return _write_inst(flags, pulse, 'LOOP', num_loops, length)

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
        return _write_inst(flags, pulse, 'END_LOOP', addr, length)

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
        return _write_inst(flags, pulse, 'JSR', addr, length)

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
        return _write_inst(flags, pulse, 'RTS', 0, length)

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
        return _write_inst(flags, pulse, 'BRANCH', addr, length)

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
        return _write_inst(flags, pulse, 'LONG_DELAY', delay, length)

    @staticmethod
    def wait_inst(flags, pulse, length):
        """Sends a WAIT instruction to a PulseBlaster. Program execution stops
        and waits for a software or hardware trigger. Execution continues to
        next instruction after receipt of trigger. The latency is equal to the
        delay value entered in the WAIT instruction line, plus a fixed delay of
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
        return _write_inst(flags, pulse, 'WAIT', 0, length)


#############
## Private ##
#############

from instrument.pulseblaster import pb_inst_pbonly

def _write_inst(flags, pulse, inst, inst_data, length):
    """Writes an instruction to a PulseBlasterESR-PRO board. Raises an
    InstrumentError if the instruction could not be written to the board.

    Should not be called outside of this module.

    Parameters:
      - flags (int): Bit field specifying which flags are set to high.
      - pulse (str): A pulse period, as specified by the `pulses` dictionary.
      - inst (str): An instruction, as specified by the `opcodes` dictionary.
      - inst_data (int): Data associated with an instuction.
      - length (float): Length of the instruction in nanoseconds.

    Returns:
      - int: Address of the created instruction.

    Raises:
      - InstrumentError
    """
    assert inst in PulseBlasterESRPRO.opcodes
    assert pulse in PulseBlasterESRPRO.pulses

    if (flags >> FLAGS_SIZE) != 0:
        raise InstrumentError('{0} instruction flag ({1}) out of bounds.'.format(
                inst, hex(flags)))
    if (inst_data >> INST_DATA_SIZE) != 0:
        raise InstrumentError('{0} instruction data ({1}) out of bounds.'.format(
                inst, hex(inst_data)))

    addr = pb_inst_pbonly(
            flags | PulseBlasterESRPRO.pulses[pulse],
            PulseBlasterESRPRO.opcodes[inst],
            inst_data,
            length,
    )

    if addr < 0:
        raise InstrumentError('could not write {0} instruction: {1}'.format(
                inst, PulseBlasterESRPRO.pb_get_error()))
    return addr

