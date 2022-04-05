import ctypes
import platform
import subprocess

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


def openTerminal():
    if platform.system() == "Windows":
        cmd = 'cmd'
    elif platform.system() == "Linux":
        cmd = 'gnome-terminal'
    else:
        cmd = 'open -a Terminal'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    if err:
        return err
    else:
        return out