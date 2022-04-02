
# 字典拆分，每块多个元素
def dictSplit(dicts, n):
    result = []
    ret = []
    p = sorted([(k, v) for k, v in dicts.items()], reverse=True)
    s = set()
    for i in p:
        s.add(i[1])
    for i in sorted(s, reverse=True)[:n]:
        for j in p:
            if j[1] == i:
                result.append(j)
    for r in result:
        ret.append(r[0])
    return ret


# 字典排序，支持正序和倒序
def dictSort(dicts, reverse=False):
    return sorted(dicts.items(), key=lambda x: x[1], reverse=reverse)
