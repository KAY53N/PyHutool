=====================
Gui Control Functions
=====================

The Screen and Mouse Position Function
======================================

Locations on your screen are referred to by X and Y Cartesian coordinates. The X coordinate starts at 0 on the left side and increases going right. Unlike in mathematics, the Y coordinate starts at 0 on the top and increases going down.

.. code::

    0,0       X increases -->
    +---------------------------+
    |                           | Y increases
    |                           |     |
    |   1920 x 1080 screen      |     |
    |                           |     V
    |                           |
    |                           |
    +---------------------------+ 1919, 1079

The pixel at the top-left corner is at coordinates 0, 0. If your screen's resolution is 1920 x 1080, the pixel in the lower right corner will be 1919, 1079 (since the coordinates begin at 0, not 1).

The screen resolution size is returned by the ``size()`` function as a tuple of two integers. The current X and Y coordinates of the mouse cursor are returned by the ``position()`` function.

For example:

.. code:: python

    >>> from pyhutool.gui import Mouse

    >>> Mouse.size() # Size(width=1440, height=900)
    >>> Mouse.position() # Point(x=293, y=605)


Mouse Clicks Function
=====================

.. code:: python

    >>> from pyhutool.gui import Mouse
    >>> Mouse.click(500, 500)
    >>> size = Mouse.size()
    >>> position = Mouse.position()
    >>> Mouse.leftClick(500, 500)


The write Function
==================
The primary keyboard function is write(). This function will type the characters in the string that is passed. To add a delay interval in between pressing each character key, pass an int or float for the interval keyword argument.
For example:

.. code:: python

    >>> from pyhutool.gui import Keyboard
    >>> Keyboard.typewrite('hello world', 0.2)

The press, keyDown, and keyUp Functions
=======================================
To press these keys, call the press() function and pass it a string from the pyhutool.KEYBOARD_KEYS such as enter, esc, f1
For example:

.. code:: python

    >>> from pyhutool.gui import Keyboard

    >>> Keyboard.keyDown('h')
    >>> Keyboard.keyUp('h')

    >>> Keyboard.press('enter')

The hotkey Function
===================
To make pressing hotkeys or keyboard shortcuts convenient, the hotkey() can be passed several key strings which will be pressed down in order, and then released in reverse order. This code:

.. code:: python

    >>> from pyhutool.gui import Keyboard
    >>> Keyboard.hotkey('ctrl', 'shift', 'esc')


The screenshot Function
=======================
Calling screenshot() will return an Image object (see the Pillow or PIL module documentation for details). Passing a string of a filename will save the screenshot to a file as well as return it as an Image object.

.. code:: python

    >>> from pyhutool.gui import Screenshot

    >>> Screenshot.screenshot('test.png')
    >>> Screenshot.screenshot('test.png', region=(0,0, 300, 400))
    >>> Screenshot.screenshot('test.png')
    >>> Screenshot.screenshot('test.png', region=(0,0, 300, 400))


The Locate Functions
====================
Find coordinates in the screen based on the feature image

.. code:: python

    >>> from pyhutool.gui import Screenshot
    >>> locate = Screenshot.locateOnScreen('img_1.png')