import importlib

from instrument import Instrument

class Engine(object):
    """Experiment Engine"""

    def __init__(self):
        self.logger = None
        self.data = None
        self.ui = None

    def run_experiment(self, experiment, **kwargs):
        """Runs an experiment.

        Parameters:
          - experiment (Experiment): An `Experiment` class.
        """
        # TODO(Jeffrey):
        #  - Error handling
        #  - Save data to file

        # Setup Engine
        self.logger = EngineLogger()
        self.data = ExperimentData
        self.connect_instruments(experiment)
        Instrument.num_instruments = 0

        # Run experiment
        experiment = experiment(**kwargs)
        experiment.setup()
        experiment.run()

        # Analyze Data
        experiment.analyze(self.data)
    
    def connect_instruments(self, experiment):
        for instrument in experiment.instruments:
            instrument = getattr(experiment, instrument)
            instrument.engine = self
            instrument._connect()

class EngineLogger(object):
    """Experiment log.

    An experiment log, for debugging purposes.
    """
    pass

class ExperimentData(object):
    """Experiment data

    """
    pass

