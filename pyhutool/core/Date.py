import datetime
from datetime import timedelta


# 根据字符串生日和日期计算年龄
def getAgeByBirthday(birthday):
    if birthday is None:
        return 0
    try:
        birthday = datetime.datetime.strptime(birthday, '%Y-%m-%d')
    except:
        return 0
    today = datetime.datetime.now()
    return (today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day)))


# 比较两个字符串日期是否为同一天
def isSameDay(date1, date2):
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')
    return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year


# 比较两个日期是否为同一月
def isSameMonth(date1, date2):
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')
    return date1.month == date2.month and date1.year == date2.year


# 比较两个日期是否为同一周
def isSameWeek(date1, date2):
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')
    return date1.isocalendar()[1] == date2.isocalendar()[1] and date1.isocalendar()[0] == date2.isocalendar()[0]


# 根据时间戳返回是在多长时间以前
def getTimeAgo(timestamp):
    if timestamp is None:
        return ''
    if type(timestamp) not in [float, int]:
        return ''
    timestamp = float(timestamp)
    dt = datetime.datetime.fromtimestamp(timestamp)
    now = datetime.datetime.now()
    delta = now - dt
    if delta.days > 365:
        return '%d年前' % (delta.days / 365)
    elif delta.days > 30:
        return '%d个月前' % (delta.days / 30)
    elif delta.days > 0:
        return '%d天前' % delta.days
    elif delta.seconds > 3600:
        return '%d小时前' % (delta.seconds / 3600)
    elif delta.seconds > 60:
        return '%d分钟前' % (delta.seconds / 60)
    else:
        return '刚刚'


def getNow():
    return getDate(getNowStr())


def getNowStr():
    return getDateStr(getNowDate())


def getDate(dateStr):
    return getDateByFormat(dateStr, '%Y-%m-%d')


def getDateByFormat(dateStr, format):
    return getDateByFormatAndLocale(dateStr, format, 'zh_CN')


def getDateByFormatAndLocale(dateStr, format, locale):
    from dateutil.parser import parse
    return parse(dateStr, dayfirst=True, fuzzy=True, locale=locale, ignoretz=True, tzinfos=None, default=None,
                 normalize=False, yearfirst=False)


def getDateStr(date):
    return getDateStrByFormat(date, '%Y-%m-%d')


def getNowDate():
    from datetime import datetime
    return datetime.now()
    

def getDateStrByFormat(date, format):
    return date.strftime(format)


# ISO格式时间，如2020-12-08T09:08:57.715Z
def getISOTimestamp():
    now = datetime.datetime.utcnow()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"