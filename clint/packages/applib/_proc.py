# Copyright (c) 2010 ActiveState Software Inc. All rights reserved.

"""Process execution wrappers
"""

from __future__ import unicode_literals
import os
import sys
import time
import subprocess
from tempfile import TemporaryFile
import warnings

from applib.misc import xjoin
from applib.misc import safe_unicode

__all__ = ['run', 'RunError', 'RunNonZeroReturn', 'RunTimedout']

warnings.filterwarnings('ignore', message='.*With\-statements.*',
                        category=DeprecationWarning)


class RunError(Exception):  

    def __init__(self, cmd, stdout, stderr, errors):
        self.stdout = stdout
        self.stderr = stderr

        msg = errors[:]
        msg.extend([
            'command: {0}'.format(safe_unicode(cmd)),
            'pwd: {0}'.format(xjoin(os.getcwd()))])
        
        if stderr is None:
            msg.append(
                'OUTPUT:\n{0}'.format(_limit_str(safe_unicode(stdout))))
        else:
            msg.extend([
                'STDERR:\n{0}'.format(_limit_str(safe_unicode(stderr))),
                'STDOUT:\n{0}'.format(_limit_str(safe_unicode(stdout)))])

        super(RunError, self).__init__('\n'.join(msg))


class RunNonZeroReturn(RunError):
    """The command returned non-zero exit code"""

    def __init__(self, p, cmd, stdout, stderr):
        super(RunNonZeroReturn, self).__init__(cmd, stdout, stderr, [
            'non-zero returncode: {0}'.format(p.returncode)
            ])


class RunTimedout(RunError):
    """process is taking too much time"""

    def __init__(self, cmd, timeout, stdout, stderr):
        super(RunTimedout, self).__init__(cmd, stdout, stderr, [
            'timed out; ergo process is terminated',
            'seconds elapsed: {0}'.format(timeout),
            ])

    
# TODO: support for incremental results (sometimes a process run for a few
# minutes, but we need to send the stdout as soon as it appears.
def run(cmd, merge_streams=False, timeout=None, env=None):
    """Improved replacement for commands.getoutput()

    The following features are implemented:

     - timeout (in seconds)
     - support for merged streams (stdout+stderr together)
     
    `cmd` can be a full command string, or list of prog/args.

    Note that returned data is of *undecoded* str/bytes type (not unicode)

    Return (stdout, stderr)
    """
    if isinstance(cmd, (list, tuple)):
        shell = False
    else:
        shell = True
        # Fix for cmd.exe quote issue. See comment #3 and #4 in
        # http://firefly.activestate.com/sridharr/pypm/ticket/126#comment:3
        if sys.platform.startswith('win') and cmd.startswith('"'):
            cmd = '"{0}"'.format(cmd)

    # redirect stdout and stderr to temporary *files*
    with TemporaryFile() as outf:
        with TemporaryFile() as errf:
            p = subprocess.Popen(cmd, env=env, shell=shell, stdout=outf,
                                 stderr=outf if merge_streams else errf)
    
            if timeout is None:
                p.wait()
            else:
                # poll for terminated status till timeout is reached
                t_nought = time.time()
                seconds_passed = 0
                while True:
                    if p.poll() is not None:
                        break
                    seconds_passed = time.time() - t_nought
                    if timeout and seconds_passed > timeout:
                        p.terminate()
                        raise RunTimedout(
                            cmd, timeout,
                            _read_tmpfd(outf),
                            None if merge_streams else _read_tmpfd(errf))
                    time.sleep(0.1)

            # the process has exited by now; nothing will to be written to
            # outfd/errfd anymore.
            stdout = _read_tmpfd(outf)
            stderr = _read_tmpfd(errf)

    if p.returncode != 0:
        raise RunNonZeroReturn(p, cmd, stdout, None if merge_streams else stderr)
    else:
        return stdout, stderr


def _read_tmpfd(fil):
    """Read from a temporary file object

    Call this method only when nothing more will be written to the temporary
    file - i.e., all the writing has already been done.
    """
    fil.seek(0)
    return fil.read()


def _limit_str(s, maxchars=80*15):
    if len(s) > maxchars:
        return '[...]\n' + s[-maxchars:]
    return s
    

def _disable_windows_error_popup():
    """Set error mode to disable Windows error popup
    
    This setting is effective for current process and all the child processes
    """
    # disable nasty critical error pop-ups on Windows
    import win32api, win32con
    win32api.SetErrorMode(win32con.SEM_FAILCRITICALERRORS |
                          win32con.SEM_NOOPENFILEERRORBOX)
if sys.platform.startswith('win'):
    try:
        import win32api
    except ImportError:
        pass # XXX: this means, you will get annoying popups
    else:
        _disable_windows_error_popup()
