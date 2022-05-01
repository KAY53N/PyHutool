import sys


def getWindowTitle():
    if sys.platform == 'win32':
        import win32gui
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    elif sys.platform == 'darwin':
        import subprocess
        return subprocess.check_output(['osascript', '-e', 'tell application "System Events" to get name of first process whose frontmost is true'])
    else:
        raise NotImplementedError('platform not supported')


def getActiveWindowTitle():
    # 兼容win和linux、mac
    if sys.platform == 'win32':
        from win32gui import GetWindowText, GetForegroundWindow
        return GetWindowText(GetForegroundWindow())
    elif sys.platform == 'darwin':
        from AppKit import NSWorkspace
        return NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    else:
        return None