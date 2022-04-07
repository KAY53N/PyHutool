import random

# 生成手机号码
def generate_phone():
    phone = '1'
    for i in range(9):
        phone += str(random.randint(0, 9))
    return phone

