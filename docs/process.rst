============
Process
============

Query whether the specified program is running
-------

.. code:: python

    >>> from pyhutool import Process

    >>> Process.checkAppIsOpen('idea.exe')


Query the detailed information of the specified process
-------

.. code:: python

    >>> from pyhutool import Process

    >>> Process.getProcessDetail('idea.exe')


Get PID based on process name, or get process name based on PID
-------

.. code:: python

    >>> from pyhutool import Process

    >>> Process.getPidByName(1)
    >>> Process.getNameByPid('idea.exe')