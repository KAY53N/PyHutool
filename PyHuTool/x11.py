import sys
import os
from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
import Xlib.XK

from PyHuTool import isShiftCharacter
from PyHuTool.Const import _const

BUTTON_NAME_MAPPING = {_const.LEFT: 1, _const.MIDDLE: 2, _const.RIGHT: 3, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}


if sys.platform in ('java', 'darwin', 'win32'):
    raise Exception('The pyhutool_x11 module should only be loaded on a Unix system that supports X11.')

def _position():
    coord = _display.screen().root.query_pointer()._data
    return coord["root_x"], coord["root_y"]


def _size():
    return _display.screen().width_in_pixels, _display.screen().height_in_pixels


def _vscroll(clicks, x=None, y=None):
    clicks = int(clicks)
    if clicks == 0:
        return
    elif clicks > 0:
        button = 4 # scroll up
    else:
        button = 5 # scroll down

    for i in range(abs(clicks)):
        _click(x, y, button=button)


def _hscroll(clicks, x=None, y=None):
    clicks = int(clicks)
    if clicks == 0:
        return
    elif clicks > 0:
        button = 7 # scroll right
    else:
        button = 6 # scroll left

    for i in range(abs(clicks)):
        _click(x, y, button=button)


def _scroll(clicks, x=None, y=None):
    return _vscroll(clicks, x, y)


def _click(x, y, button):
    assert button in BUTTON_NAME_MAPPING.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
    button = BUTTON_NAME_MAPPING[button]

    _mouseDown(x, y, button)
    _mouseUp(x, y, button)


def _moveTo(x, y):
    fake_input(_display, X.MotionNotify, x=x, y=y)
    _display.sync()


def _mouseDown(x, y, button):
    _moveTo(x, y)
    assert button in BUTTON_NAME_MAPPING.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
    button = BUTTON_NAME_MAPPING[button]
    fake_input(_display, X.ButtonPress, button)
    _display.sync()


def _mouseUp(x, y, button):
    _moveTo(x, y)
    assert button in BUTTON_NAME_MAPPING.keys(), "button argument not in ('left', 'middle', 'right', 4, 5, 6, 7)"
    button = BUTTON_NAME_MAPPING[button]
    fake_input(_display, X.ButtonRelease, button)
    _display.sync()


def _keyDown(key):
    if key not in keyboardMapping or keyboardMapping[key] is None:
        return

    if type(key) == int:
        fake_input(_display, X.KeyPress, key)
        _display.sync()
        return

    needsShift = isShiftCharacter(key)
    if needsShift:
        fake_input(_display, X.KeyPress, keyboardMapping['shift'])

    fake_input(_display, X.KeyPress, keyboardMapping[key])

    if needsShift:
        fake_input(_display, X.KeyRelease, keyboardMapping['shift'])
    _display.sync()


def _keyUp(key):
    if key not in keyboardMapping or keyboardMapping[key] is None:
        return

    if type(key) == int:
        keycode = key
    else:
        keycode = keyboardMapping[key]

    fake_input(_display, X.KeyRelease, keycode)
    _display.sync()

# Taken from PyKeyboard's ctor function.
_display = Display(os.environ['DISPLAY'])

keyboardMapping = dict([(key, None) for key in _const.KEY_NAMES])
keyboardMapping.update({
    'backspace':         _display.keysym_to_keycode(Xlib.XK.string_to_keysym('BackSpace')),
    '\b':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('BackSpace')),
    'tab':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Tab')),
    'enter':             _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
    'return':            _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
    'shift':             _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Shift_L')),
    'ctrl':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Control_L')),
    'alt':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Alt_L')),
    'pause':             _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Pause')),
    'capslock':          _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Caps_Lock')),
    'esc':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Escape')),
    'escape':            _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Escape')),
    'pgup':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Up')),
    'pgdn':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Down')),
    'pageup':            _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Up')),
    'pagedown':          _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Page_Down')),
    'end':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('End')),
    'home':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Home')),
    'left':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Left')),
    'up':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Up')),
    'right':             _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Right')),
    'down':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Down')),
    'select':            _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Select')),
    'print':             _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'execute':           _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Execute')),
    'prtsc':             _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'prtscr':            _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'prntscrn':          _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'printscreen':       _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Print')),
    'insert':            _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Insert')),
    'del':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Delete')),
    'delete':            _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Delete')),
    'help':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Help')),
    'win':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Super_L')),
    'winleft':           _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Super_L')),
    'winright':          _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Super_R')),
    'apps':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Menu')),
    'num0':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_0')),
    'num1':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_1')),
    'num2':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_2')),
    'num3':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_3')),
    'num4':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_4')),
    'num5':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_5')),
    'num6':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_6')),
    'num7':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_7')),
    'num8':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_8')),
    'num9':              _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_9')),
    'multiply':          _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Multiply')),
    'add':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Add')),
    'separator':         _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Separator')),
    'subtract':          _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Subtract')),
    'decimal':           _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Decimal')),
    'divide':            _display.keysym_to_keycode(Xlib.XK.string_to_keysym('KP_Divide')),
    'f1':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F1')),
    'f2':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F2')),
    'f3':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F3')),
    'f4':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F4')),
    'f5':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F5')),
    'f6':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F6')),
    'f7':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F7')),
    'f8':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F8')),
    'f9':                _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F9')),
    'f10':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F10')),
    'f11':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F11')),
    'f12':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F12')),
    'f13':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F13')),
    'f14':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F14')),
    'f15':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F15')),
    'f16':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F16')),
    'f17':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F17')),
    'f18':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F18')),
    'f19':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F19')),
    'f20':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F20')),
    'f21':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F21')),
    'f22':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F22')),
    'f23':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F23')),
    'f24':               _display.keysym_to_keycode(Xlib.XK.string_to_keysym('F24')),
    'numlock':           _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Num_Lock')),
    'scrolllock':        _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Scroll_Lock')),
    'shiftleft':         _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Shift_L')),
    'shiftright':        _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Shift_R')),
    'ctrlleft':          _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Control_L')),
    'ctrlright':         _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Control_R')),
    'altleft':           _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Alt_L')),
    'altright':          _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Alt_R')),
    # These are added because unlike a-zA-Z0-9, the single characters do not have a
    ' ': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('space')),
    'space': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('space')),
    '\t': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Tab')),
    '\n': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),  # for some reason this needs to be cr, not lf
    '\r': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Return')),
    '\e': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('Escape')),
    '!': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('exclam')),
    '#': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('numbersign')),
    '%': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('percent')),
    '$': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('dollar')),
    '&': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('ampersand')),
    '"': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('quotedbl')),
    "'": _display.keysym_to_keycode(Xlib.XK.string_to_keysym('apostrophe')),
    '(': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('parenleft')),
    ')': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('parenright')),
    '*': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('asterisk')),
    '=': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('equal')),
    '+': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('plus')),
    ',': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('comma')),
    '-': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('minus')),
    '.': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('period')),
    '/': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('slash')),
    ':': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('colon')),
    ';': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('semicolon')),
    '<': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('less')),
    '>': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('greater')),
    '?': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('question')),
    '@': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('at')),
    '[': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('bracketleft')),
    ']': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('bracketright')),
    '\\': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('backslash')),
    '^': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('asciicircum')),
    '_': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('underscore')),
    '`': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('grave')),
    '{': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('braceleft')),
    '|': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('bar')),
    '}': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('braceright')),
    '~': _display.keysym_to_keycode(Xlib.XK.string_to_keysym('asciitilde')),
})

# Trading memory for time" populate winKB so we don't have to call VkKeyScanA each time.
for c in """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890""":
    keyboardMapping[c] = _display.keysym_to_keycode(Xlib.XK.string_to_keysym(c))
