import unittest
import random
from function import function


class TestFunction(unittest.TestCase):
    def test_01_zero(self):
        x = 0
        eps = 0.1
        expected_value = 1
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value)

    def test_02_equal(self):
        x = 0.5
        eps = 0.001
        expected_value = 1 / (1 + x ** 2)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value, delta=eps)

    def test_03_equal(self):
        x = -0.3
        eps = 1e-10
        expected_value = 1 / (1 + x ** 2)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value)

    def test_04_true(self):
        x = 0.58
        eps = 1e-15
        expected_value = 1 / (1 + x ** 2)
        value = function(x, eps)
        self.assertTrue((abs(expected_value - value) < eps))

    def test_05_true(self):
        x = 0.0002
        eps = 1e-15
        expected_value = 1 / (1 + x ** 2)
        value = function(x, eps)
        self.assertTrue(abs(expected_value - value) < eps)

    def test_06_false(self):
        x = 0.0002
        eps = 1e-15
        expected_value = 1 / (1 + x ** 2)
        value = function(x, eps)
        self.assertFalse(abs(expected_value - value) > eps)

    def test_07_less(self):
        x1 = 0.8888
        x2 = 0.9999
        eps = 1e-6
        value1 = function(x1, eps)
        value2 = function(x2, eps)
        self.assertLess(value2, value1)

    def test_08_equal_100_random_values(self):
        for _ in range(100):
            x = random.random() * 2 - 1
            x *= random.choice((-1, 1))
            eps = 1e-15
            expected_value = 1 / (1 + x ** 2)
            value = function(x, eps)
            self.assertAlmostEqual(expected_value, value)

    def test_09_raise(self):
        with self.assertRaises(AssertionError):
            function(-1, 1)
        with self.assertRaises(AssertionError):
            function(0, 0)
        with self.assertRaises(AssertionError):
            function(10, 10)

if __name__ == '__main__':
    unittest.main(verbosity=2)
