from pyhutool.gui import Mouse, Keybord, Screenshot
from pyhutool.system import Clipboard
from pyhutool.gui.Const import _const


@Mouse.click
def click(x=None, y=None, clicks=1, interval=0.0, button=_const.PRIMARY, duration=0.0, tween=Mouse.linear,
          logScreenshot=None, _pause=True):
    pass


@Mouse.click
def leftClick(x=None, y=None, interval=0.0, duration=0.0, tween=Mouse.linear, logScreenshot=None, _pause=True):
    pass


@Mouse.size
def size():
    pass


@Mouse.position
def position():
    pass


@Keybord.keyDown
def keyDown(key, _pause=True):
    pass


@Keybord.keyUp
def keyUp(key, _pause=True):
    pass


@Keybord.hotkey
def hotKey(*args):
    pass


@Keybord.press
def press(keys, presses=1, interval=0.0, _pause=True):
    pass


@Keybord.typewrite
def typewrite(message, interval=0.0, _pause=True):
    pass


@Screenshot.screenshot
def screenshot():
    pass


@Screenshot.locateOnScreen
def locateOnScreen(image, minSearchTime=0, **kwargs):
    pass