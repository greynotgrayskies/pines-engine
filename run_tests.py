import argparse
import importlib
import os, sys
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='engine', top_level_dir='engine')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful:
        sys.exit(1)

