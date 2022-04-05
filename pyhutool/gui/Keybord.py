# -*- coding: utf-8 -*-
import platform
import subprocess
import sys
import time
from contextlib import contextmanager

import pyhutool
from pyhutool.gui.Const import _const
import functools

if sys.platform.startswith("java"):
    raise NotImplementedError("Jython is not yet supported by PyHuTool.")
elif sys.platform == "darwin":
    from pyhutool.gui import Osx as platformModule
elif sys.platform == "win32":
    from pyhutool.gui import Win as platformModule
elif platform.system() == "Linux":
    from pyhutool import X11 as platformModule
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

def _handlePause(_pause):
    if _pause:
        assert isinstance(_const.PAUSE, int) or isinstance(_const.PAUSE, float)
        time.sleep(_const.PAUSE)


def isValidKey(key):
    return platformModule.keyboardMapping.get(key, None) != None

def keyDown(fn):
    def func(key, *args, **kwargs):
        if len(key) > 1:
            key = key.lower()
        platformModule._keyDown(key)
    return func

def keyUp(key, _pause=True):
    def func(key, *args, **kwargs):
        if len(key) > 1:
            key = key.lower()
        platformModule._keyUp(key)
    return func

@contextmanager
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
        platformModule._keyDown(k)
    try:
        yield
    finally:
        for k in keys:
            platformModule._keyUp(k)


def press(fn):
    def func(*args, **kwargs):
        params = dict(zip(fn.__code__.co_varnames, [None] * fn.__code__.co_argcount))
        params['presses'],params['interval'],params['_pause'] = fn.__defaults__
        params.update(kwargs)
        for k,v in enumerate(args):
            params[fn.__code__.co_varnames[k]] = v
        keys = params['keys']
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
        interval = float(params['interval'])
        print(params)
        for i in range(params['presses']):
            for k in keys:
                platformModule._keyDown(k)
                platformModule._keyUp(k)
            time.sleep(interval)
    return func


def typewrite(fn):
    def func(*args, **kwargs):
        message = args[0]
        params = dict(zip(fn.__code__.co_varnames, [None] * fn.__code__.co_argcount))
        params['interval'],_pause = fn.__defaults__
        params.update(kwargs)
        interval = float(params['interval'])
        for c in message:
            if len(c) > 1:
                c = c.lower()
            pyhutool.gui.press(c, _pause=False)
            time.sleep(interval)
    return func


def hotkey(*args, **kwargs):
    def func(*args, **kwargs):
        interval = float(kwargs.get("interval", 0.1))  # TODO - this should be taken out.
        for c in args:
            if len(c) > 1:
                c = c.lower()
            print(c)
            platformModule._keyDown(c)
            time.sleep(interval)
        for c in reversed(args):
            if len(c) > 1:
                c = c.lower()
            platformModule._keyUp(c)
            time.sleep(interval)
    return func


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