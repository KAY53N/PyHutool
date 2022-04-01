

Welcome to PyHuTool's documentation!
=====================================

Examples
========

.. code:: python

    >>> from pyhutool import Mouse
    >>> from pyhutool import Keybord
    >>> from pyhutool import Screenshot
    >>> from pyhutool import QRCode

    >>> Mouse.click(500, 500)
    >>> size = Mouse.size()
    >>> position = Mouse.position()
    >>> Mouse.leftClick(500, 500)

    >>> Keybord.keyDown('h')
    >>> Keybord.keyUp('h')
    >>> Keybord.hotkey('ctrl', 'c')
    >>> Keybord.press('h')
    >>> Keybord.typewrite('hello world')

This example drags the mouse in a square spiral shape in MS Paint (or any graphics drawing program):