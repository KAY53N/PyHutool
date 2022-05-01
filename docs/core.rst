======================
Core Control Functions
======================

Compress Functions
===================
Compressed file related functions

.. code:: python

    >>> from pyhutool.core import Compress
    >>> Compress.Zip.create_zip('/tmp', './zip.zip', 'password') # 压缩文件
    >>> Compress.Zip.unzip('./zip.zip', '/tmp/') # 解压缩文件
    >>> Compress.Zip.zip_content('./zip.zip') # 压缩文件内容
    >>> Compress.Zip.unzip_file('./zip.zip', '1.png', './1.png') # 解压缩文件内指定文件

Convert Functions
=================

type conversion

.. code:: python

    >>> Convert.convert('123', 'tuple') # ('1', '2', '3')

convert to string
.. code:: python

    >>> Convert.to_str(0x10) # '16'

convert bytes to int

.. code:: python

    >>> Convert.bytes2int(bytes([1,2,3,4])) # 16909060


Underscore to CamelCase

.. code:: python

    >>> Convert.nameConvertToCamel('abc_def_ghi') # abcDefGhi

Hump to underscore

.. code:: python

    >>> Convert.nameConvertToSnake('abcDefGhi') # abc_def_ghi


Date Functions
==============
Calculate the age of a specified birthday in a certain year

.. code:: python

    >>> Date.getAgeByBirthday('1999-01-01') # 23


Compare if two dates are the same day

.. code:: python

    >>> Date.isSameDay('1999-01-01', '1999-01-02') # False

Compare if two dates are the same month

.. code:: python

    >>> Date.isSameMonth('1999-02-01', '1999-01-02') # False

Compare if two dates are the same week

.. code:: python

    >>> Date.isSameWeek('1999-02-01', '1999-02-02') # True


Return how long ago according to the time, such as: 1 minute ago, 1 hour ago ...

.. code:: python

    >>> Date.getTimeAgo(datetime.timestamp(datetime.now())-5000) # 1小时前

ISO format time

.. code:: python

    >>> Date.getISOTimestamp() # 2020-12-08T09:08:57.715Z


Image Functions
===============

Hexadecimal color to RGB

.. code:: python

    >>> Image.hex2rgb('#ECECEC') # (236, 236, 236)


RGB to hexadecimal color

.. code:: python

    >>> Image.rgb2hex((236, 236, 236)) # #ececec


zoom image

.. code:: python

    >>> Image.resizeImage('source.png', 'target.png', (10, 10)) # Save as target.png after scaling
    >>> Image.resizeImage('icon.png', size=(15, 15)) # Replace original image after scaling


replacement color

.. code:: python

    >>> Image.replaceColor('icon2.png', '#ECECEC', '#1210FF') # replace image color


Image watermark

.. code:: python

    >>> Image.watermarkImage('WechatIMG146.jpeg', 'icon2.png', 10, 10) # Add watermark to image

Detect image type

.. code:: python

    >>> Image.detectImageType('WechatIMG146.jpeg') # jpeg


Identify the face in the picture and return the coordinates of the face

.. code:: python

    >>> Image.face_detect('me.jpg') # [[376 328 315 315]]