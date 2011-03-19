# -*- coding: utf-8 -*-

import sys

def piped_in():
    """Returns piped input via stdin, else False."""
    with sys.stdin as stdin:
        # TTY is only way to detect if stdin contains data
        if not stdin.isatty():
            return stdin.read()  
        else:
            return None