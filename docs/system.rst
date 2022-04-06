============
System Control Functions
============

copy / paste
=============================

Invoke the copy and paste functions of the system clipboard

.. code:: python

    >>> from pyhutool.system import Clipboard

    >>> Clipboard.copy('hello world')
    >>> Clipboard.paste()


Process Function
=============================

.. code:: python

    >>> from pyhutool.system import Process

    >>> Process.getProcessDetail('idea.exe')
    >>> Process.getNameByPid(1234)
    >>> Process.checkAppIsOpen("chrome")

Window Function
=============================
.. code:: python

    >>> from pyhutool.system import Window
    >>> Window.get_window_title()
    >>> Window.get_active_window_title()

System Function
=============================
.. code:: python

    >>> from pyhutool.system import Window
    >>> Window.get_window_title() # 获取当前窗口标题
    >>> Window.get_active_window_title() # 获取当前活动窗口标题

    >>> System.info() # 获取系统信息
    >>> System.metrics() # 获取当前屏幕分辨率
    >>> System.openTerminal() # 打开终端
    >>> System.keyboardLangIsEN() # 检查当前输入法是否为英文
    >>> System.cmonitorsCount() # 获取显示器数量