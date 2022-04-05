============
Keybord Control Functions
============

The write() Function
=============================
The primary keyboard function is write(). This function will type the characters in the string that is passed. To add a delay interval in between pressing each character key, pass an int or float for the interval keyword argument.
For example:
.. code:: python

    >>> from pyhutool import gui
    >>> gui.write('hello world')

The press(), keyDown(), and keyUp() Functions
=============================
To press these keys, call the press() function and pass it a string from the pyhutool.KEYBOARD_KEYS such as enter, esc, f1
For example:
.. code:: python

    >>> gui.keyDown('h')
    >>> gui.keyUp('h')
    >>> gui.press('enter')

The hotkey() Function
=============================
To make pressing hotkeys or keyboard shortcuts convenient, the hotkey() can be passed several key strings which will be pressed down in order, and then released in reverse order. This code:
.. code:: python

    >>> gui.hotkey('ctrl', 'shift', 'esc')
