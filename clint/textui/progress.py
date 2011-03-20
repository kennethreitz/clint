import sys

def progressbar(it, prefix='', size=32, hide=False):
    count = len(it)
    if count:
        def _show(_i):
            x = int(size*_i/count)
            if not hide:
                sys.stdout.write("%s[%s>%s] %i/%i\r" % (prefix, "="*x, "-"*(size-x), _i, count))
                sys.stdout.flush()

        _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    if not hide:
        sys.stdout.write("\n")
        sys.stdout.flush()
