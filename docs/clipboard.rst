============
Clipboard Control Functions
============

copy / paste
=============================

Invoke the copy and paste functions of the system clipboard

.. code:: python

    >>> from pyhutool import Clipboard

    >>> Clipboard.copy('hello world')
    >>> Clipboard.paste()