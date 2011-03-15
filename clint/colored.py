from clint.packages import colorama

"""
Simple colorama wrapper
"""

colorama.init(autoreset=True)

def black(string):
	return '%s%s' % (colorama.Fore.BLACK, string)

def red(string):
	return '%s%s' % (colorama.Fore.RED, string)

def green(string):
	return '%s%s' % (colorama.Fore.GREEN, string)

def yellow(string):
	return '%s%s' % (colorama.Fore.YELLOW, string)

def blue(string):
	return '%s%s' % (colorama.Fore.BLUE, string)

def magenta(string):
	return '%s%s' % (colorama.Fore.MAGENTA, string)

def cyan(string):
	return '%s%s' % (colorama.Fore.CYAN, string)

def white(string):
	return '%s%s' % (colorama.Fore.WHITE, string)
