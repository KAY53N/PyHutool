

class Convert:
    # byte[]转int值
    @staticmethod
    def bytes2int(bytes):
        value = 0
        for b in bytes:
            value = value * 256 + int(b)
        return value

    # int值转byte[]
    @staticmethod
    def int2bytes(value):
        bytes = []
        for i in range(4):
            bytes.append(value >> (24 - i * 8) & 0xFF)
        return bytes

    # byte转无符号int
    @staticmethod
    def byte2uint(b):
        return b & 0xFF

    # 数字中文表示形式转数字
    @staticmethod
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
    @staticmethod
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

    # 给定字符串转换字符编码
    # 如果参数为空，则返回原字符串，不报错
    @staticmethod
    def to_str(value, encoding='utf-8'):
        if value is None:
            return value
        if isinstance(value, str):
            return value
        if isinstance(value, bytes):
            return value.decode(encoding)
        return str(value)

    # 金额转为中文形式
    @staticmethod
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
            return '零元' + Convert.number2chinese(money)
        if len(money) == 3:
            return '零' + Convert.number2chinese(money)
        if len(money) == 4:
            return Convert.number2chinese(money[0]) + '元' + Convert.number2chinese(money[1:])
        if len(money) == 5:
            return Convert.number2chinese(money[0]) + '十' + Convert.number2chinese(money[1:])
        if len(money) == 6:
            return Convert.number2chinese(money[0]) + '百' + Convert.number2chinese(money[1:])
        if len(money) == 7:
            return Convert.number2chinese(money[0]) + '千' + Convert.number2chinese(money[1:])
        if len(money) == 8:
            return Convert.number2chinese(money[0]) + '万' + Convert.number2chinese(money[1:])
        if len(money) == 9:
            return Convert.number2chinese(money[0]) + '十万' + Convert.number2chinese(money[1:])
        if len(money) == 10:
            return Convert.number2chinese(money[0]) + '百万' + Convert.number2chinese(money[1:])
        if len(money) == 11:
            return Convert.number2chinese(money[0]) + '千万' + Convert.number2chinese(money[1:])
        if len(money) == 12:
            return Convert.number2chinese(money[0]) + '亿' + Convert.number2chinese(money[1:])
        if len(money) == 13:
            return Convert.number2chinese(money[0]) + '十亿' + Convert.number2chinese(money[1:])
        if len(money) == 14:
            return Convert.number2chinese(money[0]) + '百亿' + Convert.number2chinese(money[1:])
        if len(money) == 15:
            return Convert.number2chinese(money[0]) + '千亿' + Convert.number2chinese(money[1:])
        if len(money) == 16:
            return Convert.number2chinese(money[0]) + '万亿' + Convert.number2chinese(money[1:])
        if len(money) == 17:
            return Convert.number2chinese(money[0]) + '十万亿' + Convert.number2chinese(money[1:])
        if len(money) == 18:
            return Convert.number2chinese(money[0]) + '百万亿' + Convert.number2chinese(money[1:])
        if len(money) == 19:
            return Convert.number2chinese(money[0]) + '千万亿' + Convert.number2chinese(money[1:])
        return money

    @staticmethod
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
