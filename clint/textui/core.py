# -*- coding: utf-8 -*-

"""
x

"""

import sys
from contextlib import contextmanager


STDOUT = sys.stdout.write
STDERR = sys.stderr.write

class Puts(object):
    class Borg(object):
        """All instances of Borg have the same value."""
        _shared_state = {}
        def __new__(cls, *a, **k):
            obj = object.__new__(cls, *a, **k)
            obj.__dict__ = cls._shared_state
            return obj
        def __init__(self):
            self.indent_level = 0
            self.indent_str = ''
            
    shared = Borg()
    
    def __init__(self, indent=0, quote=' ', indent_char=' '):
        # self.shared = Borg()
        self.indent = indent
        self.indent_char = indent_char
        self.indent_quote = quote
        self.shared.indent_level += indent
        self.shared.indent_str += ''.join((
            self.indent_quote,
            (self.indent_char * (self.indent - len(self.indent_quote))),
            ))
        
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.shared.indent_level += (-1 * self.indent)
        self.indent_quote = ''
        self.shared.indent_str = self.shared.indent_str[:(-1 * self.indent)]
        self.indent = 0
        
    def __call__(self, x, newline=True):
        _str = ''.join((
            self.shared.indent_str,
            x,
            '\n' if newline else ''
            ))
        STDOUT(_str)
        


def _out(stream, s, newline):
    
    terminator = '\n' if newline else ''
    
    stream('%s%s' % (s, terminator))
    

def puts(s, newline=True):
    """Prints given string to stdout."""
    _out(STDOUT, s, newline)


def puts_err(s, newline=True):
    """Prints given string to stderr."""
    _out(STDERR, s, newline)


def indent(indent=4, quote=' '):
    return Puts(indent=indent, quote=quote)


@contextmanager
def maxwidth(x=None):
    # if none, detect from applib
    print x