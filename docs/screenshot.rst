============
Screenshot Functions
============

The screenshot() Function
=============================
Calling screenshot() will return an Image object (see the Pillow or PIL module documentation for details). Passing a string of a filename will save the screenshot to a file as well as return it as an Image object.
.. code:: python

    >>> from pyhutool import gui
    >>> im = gui.screenshot('test.png')
    >>> im2 = gui.screenshot('test.png', region=(0,0, 300, 400))
    >>> im = gui.screenshot('test.png')
    >>> im2 = gui.screenshot('test.png', region=(0,0, 300, 400))


The Locate Functions
=============================
Find coordinates in the screen based on the feature image
.. code:: python

    >>> from pyhutool import gui
    >>> locate = gui.locateOnScreen('img_1.png')