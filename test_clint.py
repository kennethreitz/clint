#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Clint Test Suite."""

import unittest


class TablibTestCase(unittest.TestCas):
    """Tablib test cases."""

    def setUp(self):
        import clint


    def tearDown(self):
        pass


    def test_tsplit(self):
        from clint.utils import tsplit

        s = 'thing1,thing2-thing3/thing4*thing5'

        _s = tsplit(s, [',-/*'])
        self.



if __name__ == '__main__':
    unittest.main()
