
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


def nameConvertToCamel(name: str) -> str:
    """下划线转驼峰(小驼峰)"""
    return re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name)


def nameConvertToSnake(name: str) -> str:
    """驼峰转下划线"""
    if '_' not in name:
        name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
    else:
        raise ValueError(f'{name}字符中包含下划线，无法转换')
    return name.lower()