# -*- coding: utf-8 -*-

import sys

def piped():
    """Returns piped input via stdin, else False."""
    with sys.stdin as stdin:
        # TTY is only way to detect if stdin contains data
        return stdin.read() if not stdin.isatty() else None