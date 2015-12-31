import argparse
import sys

from importlib.machinery import SourceFileLoader

from engine import *
from experiment import *

# Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument('experiment', type=str, help='Path to an experiment file.')
parser.add_argument('-p', '--parameter', metavar='NAME=VAL', type=str, action='append', help='Experiment parameter')
args = parser.parse_args()

print(args.parameter)

# Load Experiment
# We use SourceFileLoader to load an experiment from an arbitrary filepath.
experiment_module = SourceFileLoader('experiment_src', args.experiment).load_module()
experiment_cls = experiment_module.__experiment__

parameters = {}
if args.parameter:
    for param in args.parameter:
        name, val = param.split('=')
        parameters[name] = val


# Run experiment
engine = Engine()
engine.run_experiment(experiment_cls, **parameters)

