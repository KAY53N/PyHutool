import ctypes
import platform

from win32con import SM_CMONITORS
from win32api import GetSystemMetrics


def cmonitorsCount():
    return GetSystemMetrics(SM_CMONITORS)


def info():
    return platform.system()


def metrics():
    return GetSystemMetrics(0), GetSystemMetrics(1)


def keyboardLangIsEN():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    curr_window = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(curr_window, 0)
    klid = user32.GetKeyboardLayout(thread_id)
    lid = klid & (2 ** 16 - 1)
    lid_hex = hex(lid)
    if lid_hex == '0x409':
        return True
    return False
