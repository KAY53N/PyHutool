import os
import sys
import wmi


def checkAppIsOpen(app_name):
    if sys.platform.startswith('win'):
        # 如果是Windows系统
        app_name = app_name.lower()
        for app in wmi.WMI().Win32_Process():
            if app.Name.lower() == app_name:
                return True
        return False
    elif sys.platform.startswith('linux'):
        # 如果是Linux系统
        for app in os.popen('ps -A'):
            if app_name in app:
                return True
        return False
    elif sys.platform.startswith('darwin'):
        # 如果是Mac系统
        for app in os.popen('ps -A'):
            if app_name in app:
                return True
        return False


# 检测进程中的应用程序详细信息，兼容Linux和Windows、Mac
def checkProcess(process_name):
    # 如果是Windows系统
    if os.name == 'nt':
        # 创建WMI连接
        c = wmi.WMI()
        # 创建系统进程查询
        process_wql = "select * from win32_process where name='%s'" % (process_name)
        # 执行查询
        process_list = c.query(process_wql)
        # 返回查询结果
        return process_list
    # 如果是Linux系统
    elif os.name == 'posix':
        # 创建系统进程查询
        process_command = "ps -A | grep %s" % (process_name)
        # 执行查询
        process_list = os.popen(process_command).readlines()
        # 返回查询结果
        return process_list
    # 如果是Mac系统
    elif os.name == 'mac':
        # 创建系统进程查询
        process_command = "ps -A | grep %s" % (process_name)
        # 执行查询
        process_list = os.popen(process_command).readlines()
        # 返回查询结果
        return process_list


# 根据应用名称查询PID函数，兼容多种系统
def get_pid_by_name(name):
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


# 根据PID查询应用名称函数，兼容多种系统
def get_name_by_pid(pid):
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