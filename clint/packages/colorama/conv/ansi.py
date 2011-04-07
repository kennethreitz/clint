"""
ANSI 16-color conversion utilities.
"""
# Wladimir van der Laan, 2011
#
# The original ansi colors are defined as follows
#
#   0   black 
#   1   red
#   2   green
#   3   brown (green+red)
#   4   blue
#   5   magenta (blue+red)
#   6   cyan (blue+green)
#   7   white
#
# However, the exact RGB mappings depend on the terminal that
# is used.
# In addition to these colors, nearly all terminals support 8 
# colors that are simply brighter versions of the defined colors.

_colors = [
    (0,0,0),
    (128,0,0),
    (0,128,0),
    (128,128,0),
    (0,0,128),
    (128,0,128),
    (0,128,128),
    (192,192,192),
    (128,128,128),
    (255,0,0),
    (0,255,0),
    (255,255,0),
    (0,0,255),
    (255,0,255),
    (0,255,255),
    (255,255,255)
    ]

def to_rgb(color):
    """
    Convert ANSI color tuple (color_id, bright) to RGB tuple.
    Raise `ValueError` in case of invalid color spec.
    """
    color = (color[1]<<3)|color[0]
    try:
        return _colors[color]
    except IndexError:
        raise ValueError("Color %i out of range" % color)

def from_rgb(rgb):
    """
    Convert RGB tuple to ANSI color tuple (color_id, bright).
    Raise `ValueError` in case of invalid color spec.
    """
    min_d = 1000000
    closest = None
    for idx,col in enumerate(_colors):
        dr = rgb[0]-col[0]
        dg = rgb[1]-col[1]
        db = rgb[2]-col[2]
        d = dr*dr + dg*dg + db*db
        if d < min_d:
            min_d = d
            closest = idx
    return (closest&7, closest>>3)
        
    
