============
Screenshot Functions
============

The screenshot() Function
=============================
Calling screenshot() will return an Image object (see the Pillow or PIL module documentation for details). Passing a string of a filename will save the screenshot to a file as well as return it as an Image object.
.. code:: python

    >>> from pyhutool import Screenshot
    >>> im = Screenshot.screenshot('test.png')
    >>> im2 = Screenshot.screenshot('test.png', region=(0,0, 300, 400))


The Locate Functions
=============================
Find coordinates in the screen based on the feature image
.. code:: python

    >>> from pyhutool import Screenshot
    >>> locate = Screenshot.locateOnScreen('img_1.png')