import re


def isPhoneNumber(text):
    x = re.match(r'^1[3-9]\d{9}$', text)
    if x:
        return True
    else:
        return False


def isEmail(text):
    x = re.match(r'^[\w]+@[\w]+\.[\w]+$', text)
    if x:
        return True
    else:
        return False


def isURL(text):
    x = re.match(r'^http://[\w]+\.[\w]+$', text)
    if x:
        return True
    else:
        return False


def isDate(text):
    x = re.match(r'^\d{4}-\d{2}-\d{2}$', text)
    if x:
        return True
    else:
        return False


def isIP(text):
    x = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', text)
    if x:
        return True
    else:
        return False


def isMAC(text):
    x = re.match(r'^[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}$', text)
    if x:
        return True
    else:
        return False


def isIPv6(text):
    x = re.match(r'^[0-9a-fA-F]{4}:[0-9a-fA-F]{4}:[0-9a-fA-F]{4}:[0-9a-fA-F]{4}:[0-9a-fA-F]{4}:[0-9a-fA-F]{4}:[0-9a-fA-F]{4}:[0-9a-fA-F]{4}$', text)
    if x:
        return True
    else:
        return False


def isIPv4(text):
    x = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', text)
    if x:
        return True
    else:
        return False


# 是否存在中文
def isChinese(text):
    x = re.match(r'^[\u4e00-\u9fa5]+$', text)
    if x:
        return True
    else:
        return False


# 是否存在英文
def isEnglish(text):
    x = re.match(r'^[a-zA-Z]+$', text)
    if x:
        return True
    else:
        return False


# 是否存在数字
def isNumber(text):
    x = re.match(r'^[0-9]+$', text)
    if x:
        return True
    else:
        return False


# 是否存在符号
def isSymbol(text):
    x = re.match(r'^[\W]+$', text)
    if x:
        return True
    else:
        return False


# 是否包含网址
def isContainURL(text):
    x = re.search(r'http://[\w]+\.[\w]+', text)
    if x:
        return True
    else:
        return False


# 匹配空白行
def isBlankLine(text):
    x = re.match(r'^\s*$', text)
    if x:
        return True
    else:
        return False


# 匹配QQ号码
def isQQ(text):
    x = re.match(r'^[1-9][0-9]{4,}$', text)
    if x:
        return True
    else:
        return False


# 匹配身份证号码
def isIDCard(text):
    x = re.match(r'^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$', text)
    if x:
        return True
    else:
        return False


# 匹配银行卡号
def isBankCard(text):
    x = re.match(r'^[1-9]\d{14,18}$', text)
    if x:
        return True
    else:
        return False


# 匹配邮政编码
def isPostCode(text):
    x = re.match(r'^[1-9]\d{5}$', text)
    if x:
        return True
    else:
        return False


# 匹配日期时间
def isDateTime(text):
    x = re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', text)
    if x:
        return True
    else:
        return False


# 匹配Unicode字符
def isUnicode(text):
    x = re.match(r'^[\u4e00-\u9fa5]+$', text)
    if x:
        return True
    else:
        return False

