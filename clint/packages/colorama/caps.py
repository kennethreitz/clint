from .conv import xterm256
from .conv import ansi

class _Base(object):
    """
    Base 16-color ANSI. 
    All ANSI terminals as well as Windows support this.
    """
    def fg(self, rgb):
        (colid, bright) = ansi.from_rgb(rgb)
        if bright:
            return (1, 30 + colid)
        else:
            return (30 + colid,)

    def bg(self, rgb):
        (colid, bright) = ansi.from_rgb(rgb)
        # Ignore brightness for background?
        return (40 + colid)

    def __str__():
        return "BASE"

class _XTerm256(object):
    """
    256-color terminal. Most modern terminal emulators support this.
    Putty, Gnome Terminal, and even oldies like (m)rxvt, xterm.
    """
    def fg(self, rgb):
        return (38, 5, xterm256.from_rgb(rgb))

    def bg(self, rgb):
        return (48, 5, xterm256.from_rgb(rgb))

    def __str__():
        return "XTERM256"

class _RGB(object):
    """
    Full 24-bit RGB support. 
    As far as I know, only Konsole can do this.
    """
    def fg(self, rgb):
        return (38, 2) + rgb

    def bg(self, rgb):
        return (48, 2) + rgb

    def __str__():
        return "RGB"

class ColorCapability:
    ANSI = _Base()          # Base 16-color ANSI support
    XTERM256 = _XTerm256()  # xterm256 (GNOME terminal / Putty)
    RGB = _RGB()            # Full RGB (Konsole)

# Current terminal caps, default to ANSI
capability = ColorCapability.ANSI

