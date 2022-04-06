============
Core Control Functions
============

Compress Functions
=============================
Compressed file related functions

.. code:: python

    >>> from pyhutool.core import Compress
    >>> Compress.Zip.create_zip('/tmp', './zip.zip', 'password') # 压缩文件
    >>> Compress.Zip.unzip('./zip.zip', '/tmp/') # 解压缩文件
    >>> Compress.Zip.zip_content('./zip.zip') # 压缩文件内容
    >>> Compress.Zip.unzip_file('./zip.zip', '1.png', './1.png') # 解压缩文件内指定文件

Convert Functions
=============================
Convert numbers to Chinese uppercase

.. code:: python

    >>> Convert.number2chinese('123456')

type conversion

.. code:: python

    >>> Convert.convert('123', 'tuple')

convert to string
.. code:: python

    >>> Convert.to_str(0x00)

convert byte to unit

.. code:: python

    >>> Convert.byte2uint(b'\x01\x02\x03\x04')

convert bytes to int

.. code:: python

    >>> Convert.bytes2int(bytes([1,2,3,4]))

Chinese capitalized amount converted into numbers

.. code:: python

    >>> Convert.chinese2number('壹万叁仟贰佰捌拾壹元整')

Convert digital amounts to Chinese uppercase

.. code:: python

    >>> Convert.money2chinese('238,567.89')


Date Functions
=============================
Calculate the age of a specified birthday in a certain year

.. code:: python

    >>> Date.getAge()

Modify the start time of the current week for a given date

.. code:: python

    >>> Date.setStartDate()


Compare if two dates are the same day

.. code:: python

    >>> Date.isSameDay

Compare if two dates are the same month

.. code:: python

    >>> Date.isSameMonth

Compare if two dates are the same week

.. code:: python

    >>> Date.isSameWeek

Get the specified date year and quarter

.. code:: python

    >>> Date.getYearAndQuarter

Get the year and quarter within the specified date range and return

.. code:: python

    >>> Date.getYearAndQuarterInRange

Return how long ago according to the time, such as: 1 second ago, 1 minute ago, 1 hour ago

.. code:: python

    >>> Date.getTimeBefore