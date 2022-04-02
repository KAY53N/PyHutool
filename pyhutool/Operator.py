import operator


def operatorExec(left, operatorStr, right):
    operatorDict = {'==': operator.eq, '>=': operator.ge}
    if operatorStr not in operatorDict:
        return False
    operator_func = operatorDict[operatorStr]
    if operator_func(left, right):
        return True
    else:
        return False