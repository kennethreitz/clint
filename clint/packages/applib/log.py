# Copyright (c) 2010 ActiveState Software Inc. All rights reserved.

"""Logging utilities and console integration

Don't use print, use ``LOG.info``. This ensures seemless integration with
application logging.
"""

import sys
import os
import stat
from os.path import expanduser, join, exists, isabs, dirname
import logging
from datetime import datetime
from contextlib import contextmanager

from applib import sh, textui, _cmdln as cmdln


if sys.hexversion > 0x03000000:
    def unicode_literal(s):
        return s # strings are unicode by default on py3
else:
    from io import open
    def unicode_literal(s):
        return s.decode('utf-8')


@cmdln.option('-v', '--verbose', action="count", dest='verbosity_level',
              default=None,
              help='-v will show tracebacks; -vv also debug messages')
class LogawareCmdln(cmdln.CmdlnWithConfigParser):
    """A Cmdln class that integrates with this modules's functionality

    1. Add -v and -vv global options: show tracebacks when sub commands throw
    them only if -v or -vv is passed by the user.

    2. Wrap all sub command methods and call `initialize` (to be defined by the
    derived class) automatically.
    """

    def __init__(self, install_console=False, default_verbosity=0, *args, **kwargs):
        """
        Arguments:
         - install_console: install console handlers in logger
        """
        cmdln.CmdlnWithConfigParser.__init__(self, *args, **kwargs)
        self.__initialized = False
        self.__install_console = install_console
        self.__default_verbosity = default_verbosity

    def initialize(self):
        """This method is called by ``bootstrapped`` - once and only once."""
        raise NotImplementedError('must be defined by the derived class')

    @contextmanager
    def bootstrapped(self):
        """Run the sub-command after bootstrapping

        It is required to wrap the sub-command code in this context, which takes
        care of the following:

          - Invokes `setup_console` passing `verbosity_level`
          - Invokes `self.initialize` automatically but no more than once.
          - Intercept unhandled exceptions and display them according to
            verbosity_level
        """
        l = logging.getLogger('')

        if not self.__initialized:
            # install console (if required) and call the `initialize` method
            # once.
            if self.__install_console:
                if self.options.verbosity_level is None:
                    self.options.verbosity_level = self.__default_verbosity
                setup_console(l, self.options.verbosity_level)
            with self.__run_safely(l):
                self.initialize()
            self.__initialized = True

        with self.__run_safely(l):
            yield

    @contextmanager
    def __run_safely(self, l):
        try:
            yield
        except KeyboardInterrupt:
            # user presses Ctrl-C to terminate the program
            l.info('') # print a new-line for the shell prompt's sake
            sys.exit(5)
        except Exception as e:
            if self.__install_console:
                # setup_console handles all exceptions; let it do so by calling
                # log.exception and exitting immediately.
                l.exception(e)
                sys.exit(1) # exit to shell
            else:
                # as setup_console is not used, raise exceptions normally.
                raise
        

def setup_console(l, verbosity_level):
    """Setup console output for logging calls"""
    l.setLevel(logging.DEBUG) # level-logic is instead in the handler

    existing_consoles = [h for h in l.handlers if isinstance(h, ConsoleHandler)]
    if existing_consoles:
        assert len(existing_consoles) == 1, \
            'more than one console installed. not possible.'
        # re-use existing console handler
        h = existing_consoles[0]
        assert h.verbosity_level == verbosity_level, \
            'already has console with different verbosity level'
    else:
        # create a new console handler
        h = ConsoleHandler(verbosity_level)
        h.setFormatter(ConsoleFormatter())
        l.addHandler(h)
        

def setup_trace(l, tracefile):
    """Trace logging calls to a standard log file

    Log file name and location will be determined based on platform.
    """
    l.setLevel(logging.DEBUG) # trace file must have >=DEBUG entries
    sh.mkdirs(dirname(tracefile))
    _rollover_log(tracefile)
    _begin_log_section(tracefile)
    h = logging.FileHandler(tracefile)
    h.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    l.addHandler(h)


@contextmanager
def handledby(l, filename, create_dirs=False, level=None, formatter=None):
    """Momentarily handle logger `l` using FileHandler

    Within the 'with' context, all logging calls made to the logger `l` will get
    written to the file `filename`. When exiting the 'with' context, this file
    is closed and the handler will be removed.
    """
    assert isabs(filename), 'not an absolute path: {0}'.format(filename)

    if create_dirs:
        sh.mkdirs(dirname(filename))

    h = logging.FileHandler(filename)
    if level:
        h.setLevel(level)
    if formatter:
        h.setFormatter(formatter)
    l.addHandler(h)

    try:
        yield
    finally:
        h.close()
        l.removeHandler(h)


@contextmanager
def archivedby(l, logs_directory, entity_name, level=None, formatter=None):
    """Like `handledby` but the log file is stored in archive.

    The exact path to the log file is determined as follows:

      $logs_directory/2009/03/24/142356_$entity_name.txt
    """
    now = datetime.now() # NOTE: this is local time, not UTC time.
    filename = join(logs_directory,
                    now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'),
                    '{0}_{1}.txt'.format(now.strftime('%H%M%S'), entity_name))
    assert not exists(filename), 'already exists: {0}'.format(filename)
    with handledby(l, filename, create_dirs=True,
                   level=level, formatter=formatter):
        yield filename


@contextmanager
def wrapped(l):
    """'With' context to intercept and log any exceptions raised"""
    try:
        yield
    except Exception as e:
        l.exception(e)
        raise


def runonconsole(l):
    """Run on console .. and exit the program appropriately.

    If an exception is raised, it is silently logged (so 


    >>> with log.run(logging.getLogger('pypm')) as retcode:
    """
    try:
        yield
    except Exception as e:
        l.exception(e)
        sys.exit(1)
    sys.exit(0)


try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


# -- internal

def _rollover_log(logfile, maxsize=(2<<20)):
    """Move $logfile to $logfile.old if its size exceeds `maxsize`"""
    if exists(logfile):
        filesize = os.stat(logfile)[stat.ST_SIZE]
        if filesize >= maxsize:
            sh.mv(logfile, logfile+'.old')


def _begin_log_section(logfile):
    """Begin a new section in the logfile

    Also write the current datetime
    """
    LINE_BUFFERED=1
    with open(logfile, 'a', LINE_BUFFERED, encoding='utf-8') as f:
        f.write(unicode_literal('\n')) # sections are separated by newline
        f.write(unicode_literal('{0}\n'.format(datetime.now())))


class ConsoleHandler(logging.StreamHandler):
    """Send messages to console

    INFO messages are sent to stdout. Other levels to stderr.

    By default, INFO/WARN/ERROR messages are sent as-it-is to console .. while
    EXCEPTION messages are pruned and shown as error unless verbosity level is
    greater than zero. If verbosity level is greater than one, then DEBUG
    messages are also shown.
    """

    def __init__(self, verbosity_level):
        logging.StreamHandler.__init__(self)
        self.stream = None # reset it; we are not going to use it anyway
        self.verbosity_level = verbosity_level

    def emit(self, record):
        if record.levelno == logging.INFO:
            self.__emit(record, sys.stdout)
        elif record.levelno == logging.WARN:
            self.__emit(record, sys.stderr)
        elif record.levelno == logging.DEBUG:
            # show DEBUG messages with verbosity_level >= 2
            if self.verbosity_level > 1:
                self.__emit(record, sys.stderr)
        elif record.levelno >= logging.ERROR:
            if record.exc_info and self.verbosity_level < 1:
                # supress full traceback with verbosity_level <= 0
                with new_record_exc_info(record, None):
                    self.__emit(record, sys.stderr)
            else:
                self.__emit(record, sys.stderr)
        else:
            raise NotImplementedError(
                "don't know about level: {0}".format(record.levelno))

    def __emit(self, record, strm):
        # override handler stream with ours (which could stdout or stderr)
        self.stream = strm

        with textui.safe_output():
            # We *trust* that `logging` module's `emit()` will always terminate the
            # message with newlines. This is essential for not breaking the progress
            # bar, if any.
            logging.StreamHandler.emit(self, record)

    def flush(self):
        # Workaround a bug in logging module
        # See:
        #   http://bugs.python.org/issue6333
        if self.stream and hasattr(self.stream, 'flush') and not self.stream.closed:
            try:
                logging.StreamHandler.flush(self)
            except IOError as e:
                if e.errno == 32:
                    # skip 'broken pipe' errors that likely occur due to
                    # killing the process on the other end of the pipe
                    # eg: piping command output to `less` and then pressing
                    # Q in the middle of it.
                    pass
                else:
                    raise


def _clear_record_traceback_cache(record):
    """Clear the traceback cache stored in `record` (LogRecord)

    Workaround for: http://bugs.python.org/issue6435
    """
    record.exc_text = None


@contextmanager
def new_record_exc_info(record, exc_info):
    """Temporarily assign `exc_info` to `record`"""
    _clear_record_traceback_cache(record)
    old_exc_info = record.exc_info
    record.exc_info = exc_info
    try:
        yield
    finally:
        record.exc_info = old_exc_info
        _clear_record_traceback_cache(record)


class ConsoleFormatter(logging.Formatter):
    """A formatter that attaches 'error:' prefix to error/critical messages"""

    def format(self, record):
        # attach 'error:' prefix to error/critical messages
        # attach 'warning:' prefix accordingly
        s = logging.Formatter.format(self, record)
        if record.levelno >= logging.ERROR:
            return 'error: {0}'.format(s)
        elif record.levelno == logging.WARNING:
            return 'warning: {0}'.format(s)
        else:
            return s

