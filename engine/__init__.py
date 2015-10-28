class Engine(object):
    """Experiment Engine"""

    def __init__(self):
        self.experiment = None
        self.logger = None
        self.data = None
        self.ui = None

    def run_experiment(self, experiment):
        """Runs an experiment.

        Parameters:
          - experiment (Experiment): An `Experiment` class.
        """
        # Initialize Engine parameters
        self.experiment = experiment()
        self.logger = EngineLogger()
        self.data = ExperimentData

        # Load Experiment File
        experiment = load_experiment_from_file(

        # Run setup

        # Run experiment

        # Run analysis

class EngineLogger(object):
    """Experiment log.

    An experiment log, for debugging purposes.
    """
    pass

class ExperimentData(object):
    """Experiment data

    """
    pass

def main():
    # Load Experiment File

    # Initialize any libraries before
    pass

