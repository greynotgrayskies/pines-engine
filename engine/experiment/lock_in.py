import numpy as np
import matplotlib.pylab as plt
import time

from experiment import *
from instrument.daq.sr830 import SR830
from instrument.mwfreqsynth.hp8673c import HP8673C
from instrument.pulseblaster.pulseblasteresrpro import PulseBlasterESRPRO

class LockInExperiment(Experiment):
    # Bad idea? Only one set of instrument for a class of experiments
    # Why not put in __init__?
    instruments = {
        'daq': SR830(
            address='',
        ),
        'mwfs': HP8673(
            address='',
        ),
        'pb': PulseBlasterESRPRO(
            clock_freq=100.0,
            board_num=0,
        ),
    }

    parameters = {}

    def setup(self, engine):
        # SR830 Setup
        self.daq.set_trigger_mode(1)        # TSTR 1
        self.daq.set_output_interface(1)    # OUTX 1

        # HP8673C Setup
        self.mwfs.set_amp(1)                # AP {num} DM
        self.mwfs.set_freq(1)               # FR {num} MZ

        # PulseBlaster Setup
        self.pb.start_programming('PULSE_PROGRAM')
        # PulseBlaster Program goes here. Not sure what it looks like though.
        self.pb.continue_inst(1, 'ON', 10e6)    # CONTINUE(flags, pulse, length (ns))
        self.pb.stop_inst(1, 'OFF', 10e6)       # STOP(flags, pulse, length(ns))

        self.pb.stop_programming()

    def run(self, engine):
        for i, freq in enumerate(np.linspace(self.lower_freq, self.upper_freq, self.num_samples)):
            # Change Frequency
            mwfs.set_freq(freq)
            time.sleep(.2)

            # Collect Data
            pulseblaster.start()
            daq.trigger()
            # Data is a list of inputs paired with outputs.
            # ...eventually there will be a cleaner way to do this.
            engine.data.append((freq, daq.get_values(1, 2)))
            pulseblaster.stop()

    @staticmethod
    def analyze(data):
        frequencies = np.asarray([data[0] for data in engine.data])
        out1 = np.asarray([data[0][0] for data in engine.data])
        out2 = np.asarray([data[0][1] for data in engine.data])

        plt.plot(frequencies, out1, frequencies, out2)
        plt.show()

__experiment__ = LockInExperiment
