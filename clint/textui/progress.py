# -*- coding: utf-8 -*-

"""
clint.textui.progress
~~~~~~~~~~~~~~~~~

This module provides the progressbar functionality.

"""

from __future__ import absolute_import

from .core import puts

import sys

BAR_TEMPLATE = '%s[%s%s] %i/%i\r'
BAR_EMPTY_CHAR = '-'
BAR_FILLED_CHAR = '='

DOTS_CHAR = '.'


def bar(it, label='', width=32, hide=False):
    """Progress iterator. Wrap your iterables with it."""
    count = len(it)
    if count:
        def _show(_i):
            x = int(width*_i/count)
            if not hide:
                puts(BAR_TEMPLATE % (
                    label, BAR_FILLED_CHAR*x, BAR_EMPTY_CHAR*(width-x), _i, count), newline=False)
                sys.stdout.flush()

        _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    if not hide:
        sys.stdout.write("\n")
        sys.stdout.flush()


def dots(it, label='', hide=False):
    """Progress iterator. Prints a dot for each item being iterated"""
    count = len(it)
    
    puts(label, newline=False)
    if count:
        def _show(_i):
            # sys.stdout.write('.')
            puts(DOTS_CHAR, newline=False)

        _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    if not hide:
        sys.stdout.write("\n")
