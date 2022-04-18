========================
System Control Functions
========================

Copy / Paste
============

Invoke the copy and paste functions of the system clipboard

.. code:: python

    >>> from pyhutool.system import Clipboard

    >>> Clipboard.copy('hello world')
    >>> Clipboard.paste()


Process Function
================

.. code:: python

    >>> from pyhutool.system import Process

    >>> Process.getProcessDetail('idea.exe')
    >>> Process.getNameByPid(1234)
    >>> Process.checkAppIsOpen("chrome")

Window Function
===============
.. code:: python

    >>> from pyhutool.system import Window
    >>> Window.get_window_title()
    >>> Window.get_active_window_title()

System Function
===============
Get the current window title

.. code:: python

    >>> Window.get_window_title()
    >>> Window.get_active_window_title()

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