import unittest

class TestInt1(unittest.TestCase):
    def test_int_1(self):
        self.assertEqual(1 + 1, 2)
        self.assertEqual(1 + 2, 3)

    def test_int_2(self):
        self.assertEqual(10 - 4, 6)
        self.assertEqual(10 - 3, 7)

class TestInt2(unittest.TestCase):
    def test_int_asdf(self):
        self.assertEqual(1, 1)

