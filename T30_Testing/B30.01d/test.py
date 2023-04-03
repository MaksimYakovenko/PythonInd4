import unittest
from function import function


class TestFunc(unittest.TestCase):
    def test_01_equal(self):
        x = 0
        eps = 0.01
        expected_value = 1
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value)

    def test_02_raise(self):
        with self.assertRaises(AssertionError):
            function(2, 0.1)
        with self.assertRaises(AssertionError):
            function(0, 0)
        with self.assertRaises(AssertionError):
            function(0.4, -0.2)

    def test_03_equal(self):
        x = 0.2
        eps = 0.0001
        expected_value = 1 / (1 + x ** 2)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value, delta=0.01)

    def test_04_equal(self):
        x = -0.1
        eps = 0.0001
        expected_value = 1 / (1 + x ** 2)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value, delta=0.001)

    def test_05_equal(self):
        x = 1e-16
        eps = 1e-17
        expected_value = 1 / (1 + x ** 2)
        value = function(x, eps)
        self.assertAlmostEqual(expected_value, value)

    def test_06_false(self):
        x = -0.1230001
        eps = 1e-17

        self.assertTrue(function(x, eps) > 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)