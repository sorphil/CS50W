import unittest

from prime import is_prime


class Tests(unittest.TestCase):
    def test_1(self):
        # Check 1 that is not prime
        self.assertFalse(is_prime(1))
        print(self.assertFalse(is_prime(1)))
    def test_2(self):
        # Check 2 that is prime
        self.assertTrue(is_prime(2))

    def test_8(self):
        # Check 8 that is not prime
        self.assertFalse(is_prime(8))

    def test_11(self):
        # Check 11 that is prime
        self.assertTrue(is_prime(11))

    def test_25(self):
        # Check 25 that is not prime
        self.assertFalse(is_prime(25))

    def test_28(self):
        # Check 28 that is not prime
        self.assertFalse(is_prime(28))

    def test_29(self):
        # Check 29 that is prime
        self.assertTrue(is_prime(29))
