import sys
sys.path.append("..")
from pyhutool import gui
from pyhutool.gui import Screenshot
from pyhutool import QRCode
import qrcode
from pyhutool.system import Clipboard

# gui.click(111, 500, interval=2.2)
# size = gui.size()
# position = gui.position()
# gui.leftClick(100, 500)
# gui.keyDown('h')
# gui.keyUp('h')
# gui.hotKey('ctrl', 'c')
# gui.press('h')
# gui.typewrite('hello world')

# gui.screenshot('test.png')
# locate = gui.locateOnScreen('icon.png')

# QRCode.createQrcode('test', 'qrcode.png')


Clipboard.copy('hello world')
Clipboard.paste()

# xx = Core.Io.tail('log.log', 50)
# for x in xx:
#     print(x)

