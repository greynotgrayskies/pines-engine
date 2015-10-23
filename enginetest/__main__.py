import argparse
import importlib
import os, sys
import unittest

if __name__ == '__main__':
    sys.path[0] = ''    # Set path to root of repo.
    loader = unittest.TestLoader()
    suite = loader.discover('')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful:
        sys.exit(1)

    """
    # Run core tests. If any of the core test suites fail, the engine test
    # should just exit, since it probably means that the instrument tests will
    # fail as well.
    core_suites = load_suites(SUITES_PATH, 'core')
    for suite in core_suites:
        failed += run_suite(suite)
    if failed > 0:
        sys.exit(failed)

    # By default runs all instrument tests, but can also run specific tests
    # instead. If instrument tests fail, no hardware tests should be run.
    instrument_suites = load_suites(SUITES_PATH, 'instrument')
    for suite in instrument_suites:
        failed += run_suite(suites)
    if failed > 0:
        sys.exit(failed)
    """

