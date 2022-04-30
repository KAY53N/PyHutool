
# byte[]转int值
import re


def bytes2int(bytes):
    value = 0
    for b in bytes:
        value = value * 256 + int(b)
    return value


# int值转byte[]
def int2bytes(value):
    bytes = []
    for i in range(4):
        bytes.append(value >> (24 - i * 8) & 0xFF)
    return bytes


# byte转无符号int
def byte2uint(b):
    return b & 0xFF

# 数字中文表示形式转数字
def chinese2number(chinese):
    chinese = chinese.replace('零', '0')
    chinese = chinese.replace('一', '1')
    chinese = chinese.replace('二', '2')
    chinese = chinese.replace('三', '3')
    chinese = chinese.replace('四', '4')
    chinese = chinese.replace('五', '5')
    chinese = chinese.replace('六', '6')
    chinese = chinese.replace('七', '7')
    chinese = chinese.replace('八', '8')
    chinese = chinese.replace('九', '9')
    chinese = chinese.replace('十', '10')
    chinese = chinese.replace('百', '100')
    chinese = chinese.replace('千', '1000')
    chinese = chinese.replace('万', '10000')
    chinese = chinese.replace('亿', '100000000')
    return chinese

# 转换值为指定类型
def convert(value, type):
    if type == 'int':
        return int(value)
    elif type == 'float':
        return float(value)
    elif type == 'str':
        return str(value)
    elif type == 'bool':
        return bool(value)
    elif type == 'list':
        return list(value)
    elif type == 'dict':
        return dict(value)
    elif type == 'tuple':
        return tuple(value)
    elif type == 'set':
        return set(value)
    elif type == 'bytes':
        return bytes(value)
    elif type == 'bytearray':
        return bytearray(value)
    elif type == 'memoryview':
        return memoryview(value)
    else:
        return value


def to_str(value, encoding='utf-8'):
    if value is None:
        return value
    if isinstance(value, str):
        return value
    if isinstance(value, bytes):
        return value.decode(encoding)
    return str(value)

# 金额转为中文形式
def money2chinese(money):
    money = str(money)
    if money.find('.') == -1:
        money = money + '.00'
    else:
        if len(money.split('.')[1]) == 1:
            money = money + '0'
    money = money.replace('.', '')
    if len(money) == 1:
        return '零元整'
    if len(money) == 2:
        return '零元' + number2chinese(money)
    if len(money) == 3:
        return '零' + number2chinese(money)
    if len(money) == 4:
        return number2chinese(money[0]) + '元' + number2chinese(money[1:])
    if len(money) == 5:
        return number2chinese(money[0]) + '十' + number2chinese(money[1:])
    if len(money) == 6:
        return number2chinese(money[0]) + '百' + number2chinese(money[1:])
    if len(money) == 7:
        return number2chinese(money[0]) + '千' + number2chinese(money[1:])
    if len(money) == 8:
        return number2chinese(money[0]) + '万' + number2chinese(money[1:])
    if len(money) == 9:
        return number2chinese(money[0]) + '十万' + number2chinese(money[1:])
    if len(money) == 10:
        return number2chinese(money[0]) + '百万' + number2chinese(money[1:])
    if len(money) == 11:
        return number2chinese(money[0]) + '千万' + number2chinese(money[1:])
    if len(money) == 12:
        return number2chinese(money[0]) + '亿' + number2chinese(money[1:])
    if len(money) == 13:
        return number2chinese(money[0]) + '十亿' + number2chinese(money[1:])
    if len(money) == 14:
        return number2chinese(money[0]) + '百亿' + number2chinese(money[1:])
    if len(money) == 15:
        return number2chinese(money[0]) + '千亿' + number2chinese(money[1:])
    if len(money) == 16:
        return number2chinese(money[0]) + '万亿' + number2chinese(money[1:])
    if len(money) == 17:
        return number2chinese(money[0]) + '十万亿' + number2chinese(money[1:])
    if len(money) == 18:
        return number2chinese(money[0]) + '百万亿' + number2chinese(money[1:])
    if len(money) == 19:
        return number2chinese(money[0]) + '千万亿' + number2chinese(money[1:])
    return money

def number2chinese(number):
    if number == '0':
        return '零'
    if number == '1':
        return '壹'
    if number == '2':
        return '贰'
    if number == '3':
        return '叁'
    if number == '4':
        return '肆'
    if number == '5':
        return '伍'
    if number == '6':
        return '陆'
    if number == '7':
        return '柒'
    if number == '8':
        return '捌'
    if number == '9':
        return '玖'
    return number


def name_convert_to_camel(name: str) -> str:
    """下划线转驼峰(小驼峰)"""
    return re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name)


def name_convert_to_snake(name: str) -> str:
    """驼峰转下划线"""
    if '_' not in name:
        name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    else:
        raise ValueError(f'{name}字符中包含下划线，无法转换')
    return name.lower()