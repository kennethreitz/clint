# -*- coding: utf-8 -*-

"""
x

"""

import sys
from contextlib import contextmanager


STDOUT = sys.stdout.write
STDERR = sys.stderr.write

class Puts(object):
    """All-knowing puts"""

    shared = dict(indent_level=0, indent_strings=[])
    
    def __init__(self, indent=0, quote='', indent_char=' '):
        # self.shared = Borg()
        self.indent = indent
        self.indent_char = indent_char
        self.indent_quote = quote
        self.indent_string = ''.join((
            str(quote),
            (self.indent_char * (indent - len(self.indent_quote))),
        ))

        # self.shared['indent_level'] += indent
        if len(self.indent_string):
            self.shared['indent_strings'].append(self.indent_string)
        # print self.shared['indent_strings']
        
    
        
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        # print 'exiting! %s' % len(self.shared['indent_strings'])
        # self.shared['indent_level'] += (-1 * self.indent)
        # self.shared['indent_level'] += (-1 * self.indent)
        # self.shared['indent_str'] =''
        # self.indent_quote = ''
        # self.indent=0
        # self.shared['indent_str'] = \
            # self.shared['indent_str'].replace(self.indent_str, '')
        # print len( self.shared['indent_str'])
        self.shared['indent_strings'].pop()
        # print len( self.shared['indent_str'])
        # print len(self.indent_str)
        # print len(self.shared['indent_str'])
        # print self.shared['indent_level']
            
        # print self.shared['indent_str']
        
    def __call__(self, s, newline=True, stream=STDOUT):
        # print self.shared['indent_level']
        _str = ''.join((
            ''.join(self.shared['indent_strings']),
            str(s),
            '\n' if newline else ''
            ))
        stream(_str)
        


def _out(stream, s, newline):
    
    terminator = '\n' if newline else ''
    
    stream('%s%s' % (s, terminator))
    

def puts(s, newline=True):
    """Prints given string to stdout."""
    Puts()(s, stream=STDOUT)


def puts_err(s, newline=True):
    """Prints given string to stderr."""
    Puts()(s, stream=STDERR)


def indent(indent=4, quote=' '):
    return Puts(indent=indent, quote=quote)


@contextmanager
def maxwidth(x=None):
    # if none, detect from applib
    print x