import os
import sys
import wmi


def checkAppIsOpen(app_name):
    if sys.platform.startswith('win'):
        app_name = app_name.lower()
        for app in wmi.WMI().Win32_Process():
            if app.Name.lower() == app_name:
                return True
        return False
    elif sys.platform.startswith('linux'):
        for app in os.popen('ps -A'):
            if app_name in app:
                return True
        return False
    elif sys.platform.startswith('darwin'):
        for app in os.popen('ps -A'):
            if app_name in app:
                return True
        return False


def getProcessDetail(process_name):
    if os.name == 'nt':
        c = wmi.WMI()
        process_wql = "select * from win32_process where name='%s'" % (process_name)
        process_list = c.query(process_wql)
        return process_list
    elif os.name == 'posix':
        process_command = "ps -A | grep %s" % (process_name)
        process_list = os.popen(process_command).readlines()
        return process_list
    elif os.name == 'mac':
        process_command = "ps -A | grep %s" % (process_name)
        process_list = os.popen(process_command).readlines()
        return process_list


def getPidByName(name):
    if name == '':
        return 0
    if os.name == 'nt':
        import _winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, sub_key)
        for i in range(0, _winreg.QueryInfoKey(key)[0]):
            k = _winreg.EnumKey(key, i)
            if name in k:
                return k
        return 0
    elif os.name == 'posix':
        import commands
        pid = commands.getoutput('ps -ef | grep "%s" | grep -v "grep" | awk \'{print $2}\'' % name)
        if pid == '':
            return 0
        else:
            return pid
    else:
        return 0


def getNameByPid(pid):
    if pid == 0:
        return ''
    if os.name == 'nt':
        import _winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, sub_key)
        for i in range(0, _winreg.QueryInfoKey(key)[0]):
            k = _winreg.EnumKey(key, i)
            if pid in k:
                return k
        return ''
    elif os.name == 'posix':
        import commands
        name = commands.getoutput('ps -ef | grep "%s" | grep -v "grep" | awk \'{print $8}\'' % pid)
        if name == '':
            return ''
        else:
            return name
    else:
        return ''