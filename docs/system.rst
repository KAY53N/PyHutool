========================
System Control Functions
========================

Copy / Paste
============

Invoke the copy and paste functions of the system clipboard

.. code:: python

    >>> from pyhutool.system import Clipboard

    >>> Clipboard.copy('hello world')
    >>> Clipboard.paste() # hello world


Process Function
================

.. code:: python

    >>> from pyhutool.system import Process
    >>> Process.getProcessDetail('idea.exe')


Window Function
===============
.. code:: python

    >>> from pyhutool.system import Window
    >>> Window.getWindowTitle()
    >>> Window.getActiveWindowTitle()

System Function
===============

Get system information

.. code:: python

    >>> System.info()

Get the current screen resolution

.. code:: python

    >>> System.metrics()

Open terminal

.. code:: python

    >>> System.openTerminal()

Get the number of monitors

.. code:: python

    >>> System.cmonitorsCount()

Check if the current input method is English

.. code:: python

    >>> System.keyboardLangIsEN()