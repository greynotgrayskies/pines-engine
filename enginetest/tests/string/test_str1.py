import unittest

class TestString1(unittest.TestCase):
    def test_string_1(self):
        self.assertEqual('asdf', 'asdf')

    def test_string_2(self):
        self.assertEqual('asdf' + 'asdf', 'asdfasdf')
