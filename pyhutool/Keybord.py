import os
import platform
import subprocess
import sys
import time
from contextlib import contextmanager
from src.Const import _const
import functools
from .Mouse import position

if sys.platform.startswith("java"):
    raise NotImplementedError("Jython is not yet supported by PyHuTool.")
elif sys.platform == "darwin":
    from . import Osx as platformModule
elif sys.platform == "win32":
    from . import Win as platformModule
elif platform.system() == "Linux":
    from . import X11 as platformModule
else:
    raise NotImplementedError("Your platform (%s) is not supported by PyHuTool." % (platform.system()))

if sys.version_info[0] == 2 or sys.version_info[0:2] in ((3, 1), (3, 2)):
    # Python 2 and 3.1 and 3.2 uses collections.Sequence
    import collections
    collectionsSequence = collections.Sequence
else:
    # Python 3.3+ uses collections.abc.Sequence
    import collections.abc
    collectionsSequence = collections.abc.Sequence  # type: ignore


FAILSAFE = True
FAILSAFE_POINTS = [(0, 0)]

def isShiftCharacter(character):
    return character.isupper() or character in set('~!@#$%^&*()_+{}|:"<>?')


def _genericPyAutoGUIChecks(wrappedFunction):
    @functools.wraps(wrappedFunction)
    def wrapper(*args, **kwargs):
        returnVal = wrappedFunction(*args, **kwargs)
        _handlePause(kwargs.get("_pause", True))
        return returnVal
    return wrapper


def _handlePause(_pause):
    if _pause:
        assert isinstance(_const.PAUSE, int) or isinstance(_const.PAUSE, float)
        time.sleep(_const.PAUSE)


def isValidKey(key):
    return platformModule.keyboardMapping.get(key, None) != None


@_genericPyAutoGUIChecks
def keyDown(key, _pause=True):
    if len(key) > 1:
        key = key.lower()
    platformModule._keyDown(key)


@_genericPyAutoGUIChecks
def keyUp(key, _pause=True):
    if len(key) > 1:
        key = key.lower()
    platformModule._keyUp(key)


@contextmanager
@_genericPyAutoGUIChecks
def hold(keys, logScreenshot=None, _pause=True):
    if type(keys) == str:
        if len(keys) > 1:
            keys = keys.lower()
        keys = [keys] # If keys is 'enter', convert it to ['enter'].
    else:
        lowerKeys = []
        for s in keys:
            if len(s) > 1:
                lowerKeys.append(s.lower())
            else:
                lowerKeys.append(s)
        keys = lowerKeys
    for k in keys:
        failSafeCheck()
        platformModule._keyDown(k)
    try:
        yield
    finally:
        for k in keys:
            failSafeCheck()
            platformModule._keyUp(k)


@_genericPyAutoGUIChecks
def press(keys, presses=1, interval=0.0, _pause=True):
    if type(keys) == str:
        if len(keys) > 1:
            keys = keys.lower()
        keys = [keys] # If keys is 'enter', convert it to ['enter'].
    else:
        lowerKeys = []
        for s in keys:
            if len(s) > 1:
                lowerKeys.append(s.lower())
            else:
                lowerKeys.append(s)
        keys = lowerKeys
    interval = float(interval)
    for i in range(presses):
        for k in keys:
            failSafeCheck()
            platformModule._keyDown(k)
            platformModule._keyUp(k)
        time.sleep(interval)


@_genericPyAutoGUIChecks
def typewrite(message, interval=0.0, _pause=True):
    interval = float(interval)  # TODO - this should be taken out.
    for c in message:
        if len(c) > 1:
            c = c.lower()
        press(c, _pause=False)
        time.sleep(interval)
        failSafeCheck()


@_genericPyAutoGUIChecks
def hotkey(*args, **kwargs):
    interval = float(kwargs.get("interval", 0.0))  # TODO - this should be taken out.
    for c in args:
        if len(c) > 1:
            c = c.lower()
        platformModule._keyDown(c)
        time.sleep(interval)
    for c in reversed(args):
        if len(c) > 1:
            c = c.lower()
        platformModule._keyUp(c)
        time.sleep(interval)


@_genericPyAutoGUIChecks
def openVirtualKeybord():
    if platform.system() == "Windows":
        cmd = 'osk'
    elif platform.system() == "Linux":
        cmd = 'xinput'
    else:
        cmd = 'osk'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        return err
    else:
        return out


@_genericPyAutoGUIChecks
def openNotepad():
    if platform.system() == "Windows":
        cmd = 'notepad'
    elif platform.system() == "Linux":
        cmd = 'gedit'
    else:
        cmd = 'notepad'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        return err
    else:
        return out


@_genericPyAutoGUIChecks
def openRegedit():
    if platform.system() == "Windows":
        cmd = 'regedit'
    else:
        cmd = 'notepad'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        return err
    else:
        return out


@_genericPyAutoGUIChecks
def openApp(apppath):
    if platform.system() == "Windows":
        cmd = 'start ' + apppath
    elif platform.system() == "Linux":
        cmd = 'xdg-open ' + apppath
    else:
        cmd = 'open ' + apppath
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        return err
    else:
        return out


# 打开终端，兼容Windows和Linux与MacOS
@_genericPyAutoGUIChecks
def openTerminal():
    if platform.system() == "Windows":
        cmd = 'cmd'
    elif platform.system() == "Linux":
        cmd = 'gnome-terminal'
    else:
        cmd = 'open -a Terminal'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        return err
    else:
        return out


def failSafeCheck():
    if FAILSAFE and tuple(position()) in FAILSAFE_POINTS:
        raise Exception(
            "PyHuTool fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set PyHuTool.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED."
        )