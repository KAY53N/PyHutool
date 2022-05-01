import os
import sys
import wmi


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
