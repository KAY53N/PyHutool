========================
Crypto Control Functions
========================

Encryption and decryption module related implementation

AES Function
============

AES encryption and decryption related functions

.. code:: python

    >>> m = b'abcdefghij'
    >>> key = b'123456'
    >>> a = AES(key)
    >>> cc = a.Encrypt(m)
    >>> mm = a.Decrypt(cc)
    >>> print(m)
    >>> print(a.K)
    >>> print_bytes_hex(cc)
    >>> print(mm)86