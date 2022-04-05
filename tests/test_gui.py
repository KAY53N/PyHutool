# -*- coding: utf-8 -*-
import platform
import sys
import time
import unittest

from twisted.python.compat import raw_input

sys.path.append("..")
from pyhutool import gui

if sys.platform == 'darwin':
    from pyhutool.gui import Osx as _platformModule
elif sys.platform == 'win32':
    from pyhutool.gui import Win as _platformModule
elif platform.system() == 'Linux':
    from pyhutool.gui import X11 as _platformModule
if sys.version_info[0] == 2 or sys.version_info[0:2] in ((3, 1), (3, 2)):
    import collections
    collectionsSequence = collections.Sequence
else:
    import collections.abc
    collectionsSequence = collections.abc.Sequence
Size = collections.namedtuple('Size', 'width height')

class TestGui(unittest.TestCase):
    def test_click(self):
        gui.click(x=100, y=100)
        time.sleep(0.5)
        x,y = gui.position()
        self.assertEqual(100, x)
        self.assertEqual(100, y)

    def test_left_click(self):
        gui.leftClick(x=200, y=100)
        time.sleep(0.5)
        x,y = gui.position()
        self.assertEqual(200, x)
        self.assertEqual(100, y)

    def test_position(self):
        gui.position(x=200, y=100)
        x,y = gui.position()
        self.assertEqual(200, x)
        self.assertEqual(100, y)

    def test_size(self):
        px,py = Size(*_platformModule._size())
        x,y = gui.size()
        self.assertEqual(px, x)
        self.assertEqual(py, y)

if __name__ == "__main__":
    unittest.main()