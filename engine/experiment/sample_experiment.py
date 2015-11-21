import sys
from experiment import *

class SampleExperiment(Experiment):
    data = []
    instruments = {}
    parameters = {
        'test': IntParameter('Test Parameter'),
    }

    def setup(self):
        print('Setting up experiment! ({0})'.format(self.test))

    def run(self):
        self.test += 1
        print('Running experiment! ({0})'.format(self.test))

    @staticmethod
    def analyze(data):
        print('Analyzing data!')

# This variable is used to specify which class should be used to run the
# experiment when this module is loaded.
__experiment__ = SampleExperiment

