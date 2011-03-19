from clint.packages import colorama

"""
Simple colorama wrapper
"""

colorama.init(autoreset=True)

def black(string):
	return '%s%s%s' % (colorama.Fore.BLACK, string, colorama.Fore.RESET)

def red(string):
	return '%s%s%s' % (colorama.Fore.RED, string, colorama.Fore.RESET)

def green(string):
	return '%s%s%s' % (colorama.Fore.GREEN, string, colorama.Fore.RESET)

def yellow(string):
	return '%s%s%s' % (colorama.Fore.YELLOW, string, colorama.Fore.RESET)

def blue(string):
	return '%s%s%s' % (colorama.Fore.BLUE, string, colorama.Fore.RESET)

def magenta(string):
	return '%s%s%s' % (colorama.Fore.MAGENTA, string, colorama.Fore.RESET)

def cyan(string):
	return '%s%s%s' % (colorama.Fore.CYAN, string, colorama.Fore.RESET)

def white(string):
	return '%s%s%s' % (colorama.Fore.WHITE, string, colorama.Fore.RESET)
