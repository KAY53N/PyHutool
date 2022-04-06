============
Process Functions
============

Query the running status of the application
=============================

.. code:: python

from pyhutool.process import Process

    >>> Process.checkAppIsOpen('idea.exe')

    >>> Process.checkAppIsOpen('idea.exe')

Get app details
=============================

.. code:: python

    >>> from pyhutool import Process

    >>> Process.getProcessDetail('idea.exe')


Get PID based on process name, or get process name based on PID
=============================

.. code:: python

    >>> from pyhutool import Process

    >>> Process.getPidByName(1)
    >>> Process.getNameByPid('idea.exe')