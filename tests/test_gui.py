# -*- coding: utf-8 -*-
import platform
import sys
import time
import unittest
sys.path.append("..")
from pyhutool.gui import Mouse, Keyboard, Screenshot

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
        Mouse.click(x=100, y=100)
        time.sleep(0.5)
        x,y = Mouse.position()
        self.assertEqual(100, x)
        self.assertEqual(100, y)

    def test_left_click(self):
        Mouse.leftClick(x=200, y=100)
        time.sleep(0.5)
        x,y = Mouse.position()
        self.assertEqual(200, x)
        self.assertEqual(100, y)

    def test_position(self):
        Mouse.position(x=200, y=100)
        time.sleep(0.5)
        x,y = Mouse.position()
        print(x, y)
        self.assertEqual(200, x)
        self.assertEqual(100, y)

    def test_size(self):
        px,py = Size(*_platformModule._size())
        x,y = Mouse.size()
        self.assertEqual(px, x)
        self.assertEqual(py, y)


if __name__ == "__main__":
    unittest.main()