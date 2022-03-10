import platform
import sys
import time
from contextlib import contextmanager
from PyHuTool.Const import _const
import functools
from .Mouse import position

if sys.platform.startswith("java"):
    raise NotImplementedError("Jython is not yet supported by PyHuTool.")
elif sys.platform == "darwin":
    from . import osx as platformModule
elif sys.platform == "win32":
    from . import win as platformModule
elif platform.system() == "Linux":
    from . import x11 as platformModule
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


def failSafeCheck():
    if FAILSAFE and tuple(position()) in FAILSAFE_POINTS:
        raise Exception(
            "PyHuTool fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set PyHuTool.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED."
        )