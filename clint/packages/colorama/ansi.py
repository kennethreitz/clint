'''
This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
'''
from . import caps

CSI = '\033['

def code_to_chars(codes):
    codes = [str(code) for code in codes]
    return CSI + (";".join(codes)) + 'm'

class AnsiCodes(object):
    def __init__(self, codes):
        for name in dir(codes):
            if not name.startswith('_'):
                value = getattr(codes, name)
                setattr(self, name, code_to_chars(value))
        self._method = codes._caps_method

    def __call__(self, code):
        if isinstance(code, basestring):
            return code
        else: # extended (pass to capability)
            return code_to_chars(getattr(caps.capability, self._method)(code))

class AnsiFore:
    _caps_method  = 'fg'
    BLACK   = (30,)
    RED     = (31,)
    GREEN   = (32,)
    YELLOW  = (33,)
    BLUE    = (34,)
    MAGENTA = (35,)
    CYAN    = (36,)
    WHITE   = (37,)
    RESET   = (39,)

class AnsiBack:
    _caps_method  = 'bg'
    BLACK   = (40,)
    RED     = (41,)
    GREEN   = (42,)
    YELLOW  = (43,)
    BLUE    = (44,)
    MAGENTA = (45,)
    CYAN    = (46,)
    WHITE   = (47,)
    RESET   = (49,)

class AnsiStyle:
    _caps_method = 'style'
    BRIGHT    = (1,)
    DIM       = (2,)
    NORMAL    = (22,)
    RESET_ALL = (0,)

Fore = AnsiCodes( AnsiFore )
Back = AnsiCodes( AnsiBack )
Style = AnsiCodes( AnsiStyle )

