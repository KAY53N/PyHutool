import sys
sys.path.append("..")
from pyhutool import Mouse
from pyhutool import Keybord
from pyhutool import Screenshot
from pyhutool import QRCode
from pyhutool import Clipboard


# Mouse.click(500, 500)
# size = Mouse.size()
# position = Mouse.position()
# Mouse.leftClick(500, 500)

# Keybord.keyDown('h')
# Keybord.keyUp('h')
# Keybord.hotkey('ctrl', 'c')
# Keybord.press('h')
# Keybord.typewrite('hello world')

# Screenshot.screenshot('test.png')
# locate = Screenshot.locateOnScreen('img_1.png')

# QRCode.createQrcode('test', 'qrcode.png')


Clipboard.copy('hello world')
Clipboard.paste()