import platform
import sys
import time
from pyhutool.gui.Const import _const

if sys.platform == 'darwin':
    from . import Osx as _platformModule
elif sys.platform == 'win32':
    from . import Win as _platformModule
elif platform.system() == 'Linux':
    from . import X11 as _platformModule
else:
    raise NotImplementedError('Your platform (%s) is not supported by PyHutool.' % (platform.system()))

if sys.version_info[0] == 2 or sys.version_info[0:2] in ((3, 1), (3, 2)):
    import collections
    collectionsSequence = collections.Sequence
else:
    import collections.abc
    collectionsSequence = collections.abc.Sequence

Point = collections.namedtuple('Point', 'x y')
Size = collections.namedtuple('Size', 'width height')


def linear(n):
    if not 0.0 <= n <= 1.0:
        raise Exception('Argument must be between 0.0 and 1.0.')
    return n


def leftClick(x=None, y=None, interval=0.0, duration=0.0, tween=linear, logScreenshot=None, _pause=True):
    click(x, y, 1, interval, _const.LEFT, duration)


try:
    import pyscreeze
    from pyscreeze import center, grab, pixel, pixelMatchesColor, screenshot

    def locate(*args, **kwargs):
        return pyscreeze.locate(*args, **kwargs)

    def locateAll(*args, **kwargs):
        return pyscreeze.locateAll(*args, **kwargs)

    def locateAllOnScreen(*args, **kwargs):
        return pyscreeze.locateAllOnScreen(*args, **kwargs)

    def locateCenterOnScreen(*args, **kwargs):
        return pyscreeze.locateCenterOnScreen(*args, **kwargs)

    def locateOnScreen(*args, **kwargs):
        return pyscreeze.locateOnScreen(*args, **kwargs)

    def locateOnWindow(*args, **kwargs):
        return pyscreeze.locateOnWindow(*args, **kwargs)



except ImportError:
    def _couldNotImportPyScreeze(*unused_args, **unsed_kwargs):
        raise Exception(
            "PyHuTool was unable to import pyscreeze. (This is likely because you're running a version of Python that Pillow (which pyscreeze depends on) doesn't support currently.) Please install this module to enable the function you tried to call."
        )

    center = _couldNotImportPyScreeze
    grab = _couldNotImportPyScreeze
    locate = _couldNotImportPyScreeze
    locateAll = _couldNotImportPyScreeze
    locateAllOnScreen = _couldNotImportPyScreeze
    locateCenterOnScreen = _couldNotImportPyScreeze
    locateOnScreen = _couldNotImportPyScreeze
    locateOnWindow = _couldNotImportPyScreeze
    pixel = _couldNotImportPyScreeze
    pixelMatchesColor = _couldNotImportPyScreeze
    screenshot = _couldNotImportPyScreeze

def _normalizeButton(button):
    button = button.lower()
    if platform.system() == "Linux":
        # Check for valid button arg on Linux:
        if button not in (_const.LEFT, _const.MIDDLE, _const.RIGHT, _const.PRIMARY, _const.SECONDARY, 1, 2, 3, 4, 5, 6, 7):
            raise Exception(
                "button argument must be one of ('left', 'middle', 'right', 'primary', 'secondary', 1, 2, 3, 4, 5, 6, 7)"
            )
    else:
        # Check for valid button arg on Windows and macOS:
        if button not in (_const.LEFT, _const.MIDDLE, _const.RIGHT, _const.PRIMARY, _const.SECONDARY, 1, 2, 3):
            raise Exception(
                "button argument must be one of ('left', 'middle', 'right', 'primary', 'secondary', 1, 2, 3)"
            )

    # TODO - Check if the primary/secondary mouse buttons have been swapped:
    if button in (_const.PRIMARY, _const.SECONDARY):
        swapped = False  # TODO - Add the operating system-specific code to detect mouse swap later.
        if swapped:
            if button == _const.PRIMARY:
                return _const.RIGHT
            elif button == _const.SECONDARY:
                return _const.LEFT
        else:
            if button == _const.PRIMARY:
                return _const.LEFT
            elif button == _const.SECONDARY:
                return _const.RIGHT

    return {_const.LEFT: _const.LEFT, _const.MIDDLE: _const.MIDDLE, _const.RIGHT: _const.RIGHT, 1: _const.LEFT, 2: _const.MIDDLE, 3: _const.RIGHT, 4: 4, 5: 5, 6: 6, 7: 7}[button]

def position(x=None, y=None):
    posx, posy = _platformModule._position()
    posx = int(posx)
    posy = int(posy)
    if x is not None:  # If set, the x parameter overrides the return value.
        posx = int(x)
    if y is not None:  # If set, the y parameter overrides the return value.
        posy = int(y)
    return Point(posx, posy)


def size():
    return Size(*_platformModule._size())


def _mouseMoveDrag(moveOrDrag, x, y, xOffset, yOffset, duration, tween=linear, button=None):
    global sleep_amount
    assert moveOrDrag in ("move", "drag"), "moveOrDrag must be in ('move', 'drag'), not %s" % (moveOrDrag)

    if sys.platform != "darwin":
        moveOrDrag = "move"  # Only OS X needs the drag event specifically.

    xOffset = int(xOffset) if xOffset is not None else 0
    yOffset = int(yOffset) if yOffset is not None else 0

    if x is None and y is None and xOffset == 0 and yOffset == 0:
        return  # Special case for no mouse movement at all.

    startx, starty = position()

    x = int(x) if x is not None else startx
    y = int(y) if y is not None else starty

    x += xOffset
    y += yOffset

    width, height = size()

    steps = [(x, y)]

    if duration > _const.MINIMUM_DURATION:
        num_steps = max(width, height)
        sleep_amount = duration / num_steps
        if sleep_amount < _const.MINIMUM_SLEEP:
            num_steps = int(duration / _const.MINIMUM_SLEEP)
            sleep_amount = duration / num_steps

        steps = [getPointOnLine(startx, starty, x, y, tween(n / num_steps)) for n in range(num_steps)]
        # Making sure the last position is the actual destination.
        steps.append((x, y))

    for tweenX, tweenY in steps:
        if len(steps) > 1:
            # A single step does not require tweening.
            time.sleep(sleep_amount)

        tweenX = int(round(tweenX))
        tweenY = int(round(tweenY))

        if moveOrDrag == "move":
            _platformModule._moveTo(tweenX, tweenY)
        elif moveOrDrag == "drag":
            _platformModule._dragTo(tweenX, tweenY, button)
        else:
            raise NotImplementedError("Unknown value of moveOrDrag: {0}".format(moveOrDrag))


def getPointOnLine(x1, y1, x2, y2, n):
    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1
    return (x, y)


def _normalizeXYArgs(firstArg, secondArg):
    if firstArg is None and secondArg is None:
        return position()
    elif isinstance(firstArg, str):
        try:
            location = locateOnScreen(firstArg)
            if location is not None:
                return center(location)
            else:
                return None
        except:
            raise Exception('ImageNotFoundException')

        return center(locateOnScreen(firstArg))

    elif isinstance(firstArg, collectionsSequence):
        if len(firstArg) == 2:
            # firstArg is a two-integer tuple: (x, y)
            if secondArg is None:
                return Point(int(firstArg[0]), int(firstArg[1]))
            else:
                raise Exception(
                    "When passing a sequence for firstArg, secondArg must not be passed (received {0}).".format(
                        repr(secondArg)
                    )
                )
        elif len(firstArg) == 4:
            # firstArg is a four-integer tuple, (left, top, width, height), we should return the center point
            if secondArg is None:
                return center(firstArg)
            else:
                raise Exception(
                    "When passing a sequence for firstArg, secondArg must not be passed and default to None (received {0}).".format(
                        repr(secondArg)
                    )
                )
        else:
            raise Exception(
                "The supplied sequence must have exactly 2 or exactly 4 elements ({0} were received).".format(
                    len(firstArg)
                )
            )
    else:
        return Point(int(firstArg), int(secondArg))  # firstArg and secondArg are just x and y number values

def click(
    x=None, y=None, clicks=1, interval=0.0, button=_const.PRIMARY, duration=0.0, tween=linear, logScreenshot=None, _pause=True
):
    button = _normalizeButton(button)
    x, y = _normalizeXYArgs(x, y)
    _mouseMoveDrag("move", x, y, 0, 0, duration)

    if sys.platform == 'darwin':
        for i in range(clicks):
            if button in (_const.LEFT, _const.MIDDLE, _const.RIGHT):
                _platformModule._multiClick(x, y, button, 1, interval)
    else:
        for i in range(clicks):
            if button in (_const.LEFT, _const.MIDDLE, _const.RIGHT):
                _platformModule._click(x, y, button)
            time.sleep(interval)