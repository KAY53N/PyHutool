============
Mouse Control Functions
============

The Screen and Mouse Position
=============================

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
    >>> from pyhutool import gui
    >>> gui.size()
    (1920, 1080)
    >>> gui.position()
    (187, 567)


Mouse Clicks
=============================

.. code:: python

    >>> from pyhutool import gui
    >>> gui.click(500, 500)
    >>> size = gui.size()
    >>> position = gui.position()
    >>> gui.leftClick(500, 500)

