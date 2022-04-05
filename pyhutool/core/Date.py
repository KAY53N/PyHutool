from datetime import timedelta


class CalendarUtil:

    # 计算相对于dateToCompare的年龄，长用于计算指定生日在某年的年龄
    @staticmethod
    def getAge(birthday, dateToCompare):
        return dateToCompare.year - birthday.year - ((dateToCompare.month, dateToCompare.day) < (birthday.month, birthday.day))

    # 修改某年的开始时间
    @staticmethod
    def setStartDate(date, year):
        return date.replace(year=year)

    # 修改给定日期当前周的开始时间
    @staticmethod
    def setStartDateOfWeek(date):
        return date - timedelta(days=date.weekday())

    # 比较两个日期是否为同一天
    @staticmethod
    def isSameDay(date1, date2):
        return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year

    # 比较两个日期是否为同一月
    @staticmethod
    def isSameMonth(date1, date2):
        return date1.month == date2.month and date1.year == date2.year

    # 比较两个日期是否为同一周
    @staticmethod
    def isSameWeek(date1, date2):
        return date1.isocalendar()[1] == date2.isocalendar()[1] and date1.year == date2.year

    # 获得指定日期年份和季度
    @staticmethod
    def getYearAndQuarter(date):
        return date.year, date.month // 3 + 1

    # 获得指定日期区间内的年份和季度并返回
    @staticmethod
    def getYearAndQuarterInRange(startDate, endDate):
        yearList = []
        quarterList = []
        while startDate <= endDate:
            yearList.append(startDate.year)
            quarterList.append(startDate.month // 3 + 1)
            startDate += timedelta(days=90)
        return yearList, quarterList

    # 根据时间返回多长时间以前，如：1秒前、1分钟前，1小时前，1天前，1个月前，1年前,中文或英文
    @staticmethod
    def getTimeBefore(date):
        now = CalendarUtil.getNow()
        delta = now - date
        if delta.days == 0:
            if delta.seconds < 60:
                return '%s秒前' % delta.seconds
            elif delta.seconds < 3600:
                return '%s分钟前' % (delta.seconds // 60)
            elif delta.seconds < 86400:
                return '%s小时前' % (delta.seconds // 3600)
        if delta.days == 1:
            return '1天前'
        if 1 < delta.days < 31:
            return '%s天前' % delta.days
        if 31 <= delta.days < 365:
            return '%s个月前' % (delta.days // 30)
        return '%s年前' % (delta.days // 365)

    @staticmethod
    def getNow():
        return CalendarUtil.getDate(CalendarUtil.getNowStr())

    @staticmethod
    def getNowStr():
        return CalendarUtil.getDateStr(CalendarUtil.getNowDate())

    @staticmethod
    def getDate(dateStr):
        return CalendarUtil.getDateByFormat(dateStr, '%Y-%m-%d')

    @staticmethod
    def getDateByFormat(dateStr, format):
        return CalendarUtil.getDateByFormatAndLocale(dateStr, format, 'zh_CN')

    @staticmethod
    def getDateByFormatAndLocale(dateStr, format, locale):
        from dateutil.parser import parse
        return parse(dateStr, dayfirst=True, fuzzy=True, locale=locale, ignoretz=True, tzinfos=None, default=None,
                     normalize=False, yearfirst=False)

    @staticmethod
    def getDateStr(date):
        return CalendarUtil.getDateStrByFormat(date, '%Y-%m-%d')

    @staticmethod
    def getDateStrByFormat(date, format):
        return date.strftime(format)

    @staticmethod
    def getDateStrByFormatAndLocale(date, format, locale):
        return date.strftime(format).replace('-', '年').replace('-', '月').replace('-', '日')

    @staticmethod
    def getDateStrByFormatAndLocaleAndTimezone(date, format, locale, timezone):
        return date.strftime(format).replace('-', '年').replace('-', '月').replace('-', '日')

    @staticmethod
    def getNowDate():
        from datetime import datetime
        return datetime.now()
    
