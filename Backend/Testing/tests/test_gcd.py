from unittest import TestCase
import unittest2
import doctest
import pytest
import tox
import hypothesis
from USML_homeworks.Backend.Testing.gcd import gcd
# from gcd import gcd


class TestGcd(TestCase):
    def test_m_or_n_less_than_0(self):
        for i in range(-1, -1001, -1):
            with self.assertRaises(ValueError):
                gcd(i, i - 20)
                gcd(i, 4)
                gcd(4, i)

    def test_m_is_null(self):
        for i in range(1, 1001):
            self.assertEqual(gcd(0, i), i)

    def test_n_is_null(self):
        for i in range(1, 1001):
            self.assertEqual(gcd(i, 0), i)

    def test_m_is_equal_n(self):
        for i in range(1, 1001):
            self.assertEqual(gcd(i, i), i)

    def test_m_and_n_is_equal_1(self):
        self.assertEqual(gcd(1, 1), 1)

    def test_m_and_n_is_even(self):
        for i in range(2, 1001, 2):
            self.assertTrue(gcd(i, i + i) % 2 == 0)
            self.assertTrue(gcd(i + i, i) % 2 == 0)

    def test_m_is_even_and_n_is_odd(self):
        for i in range(2, 1001, 2):
            self.assertTrue(gcd(i, i + (i - 1)) % 2 == 1)
            self.assertTrue(gcd(i + i, i - 1) % 2 == 1)

