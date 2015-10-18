import os, sys
import unittest

def load_tests(loader, tests, pattern):
    print('Called load_tests{0}'.format((loader, tests, pattern)))

