============
Keybord Control Functions
============

The write() Function
=============================
The primary keyboard function is write(). This function will type the characters in the string that is passed. To add a delay interval in between pressing each character key, pass an int or float for the interval keyword argument.
For example:
.. code:: python

    >>> from pyhutool import Keybord
    >>> Keybord.write('hello world')

The press(), keyDown(), and keyUp() Functions
=============================
To press these keys, call the press() function and pass it a string from the pyautogui.KEYBOARD_KEYS such as enter, esc, f1
For example:
.. code:: python

    >>> Keybord.keyDown('h')
    >>> Keybord.keyUp('h')
    >>> Keybord.press('enter')

The hotkey() Function
=============================
To make pressing hotkeys or keyboard shortcuts convenient, the hotkey() can be passed several key strings which will be pressed down in order, and then released in reverse order. This code:
.. code:: python

    >>> Keybord.hotkey('ctrl', 'shift', 'esc')
