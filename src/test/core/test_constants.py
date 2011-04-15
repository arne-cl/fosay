# -*- coding: utf-8 -*-
import unittest
from core.constants import *

class FuncsTestCase(unittest.TestCase):
    def test_eq(self):
        self.assertTrue(eq(1, None))
        self.assertTrue(eq(None, 1))
        self.assertTrue(eq(None, None))
        self.assertFalse(eq(1, 2))
        for n in range(0, 11):
            self.assertTrue(eq(n*100, n*100))

