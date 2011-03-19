# -*- coding: utf-8 -*-

"""
x

"""

import sys

STDOUT = sys.stdout.write
STDERR = sys.stderr.write

def indent(x=4):
    print x


def _out(stream, s, newline):
    
    terminator = '\n' if newline else ''
    
    stream('%s%s' % (s, terminator))
    

def puts(s, newline=True):
    """Prints given string to stdout."""
    _out(STDOUT, s, newline)


def puts_err(s, newline=True):
    """Prints given string to stderr."""
    _out(STDERR, s, newline)


def maxwidth(x=None):
    # if none, detect from applib
    print x