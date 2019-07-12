from datetime import datetime, timedelta, date
from share.db import sum_zero
from django.db.models import Count, Avg, Sum, F, FloatField


recent_days = 30
recent_months = 12
recent_years = 6


def get_daily_recent_charging_records(queryset):
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    x = []
    y = []
    for i in range(1, recent_days + 1):  # provide recent 6 month
        start_date = datetime(year=year, month=month, day=day)
        end_date = datetime(year=year, month=month, day=day, hour=23, minute=59, second=59)
        sum_energy = queryset.filter(dttfinishtime__gte=start_date, dttfinishtime__lt=end_date).aggregate(
            total=sum_zero('dblenergy'))['total']

        dt = datetime.strptime("{0}-{1}-{2}".format(year, month, day), "%Y-%m-%d")
        x.append(dt.strftime("%Y-%m-%d"))
        y.append(sum_energy)

        yesterday = start_date - timedelta(days=1)
        year = yesterday.year
        month = yesterday.month
        day = yesterday.day
    return dict(x=reversed(x), y=reversed(y))


def get_monthly_recent_charging_records(queryset):
    now = datetime.now()
    year = now.year
    month = now.month
    x = []
    y = []
    for i in range(1, recent_months + 1):  # provide recent 6 month
        start_date = datetime(year=year, month=month, day=1)
        end_date = datetime(year=year if month < 12 else year + 1, month=month + 1 if month < 12 else 1, day=1)
        sum_energy = queryset.filter(dttfinishtime__gte=start_date, dttfinishtime__lt=end_date).aggregate(
            total=sum_zero('dblenergy'))['total']

        dt = datetime.strptime("{0}-{1}".format(year, month), "%Y-%m")
        x.append(dt.strftime("%Y-%m"))
        y.append(sum_energy)

        month = month - 1 if month > 1 else 12
        year = year - 1 if month == 12 else year
    return dict(x=reversed(x), y=reversed(y))


def get_yearly_recent_charging_records(queryset):
    now = datetime.now()
    year = now.year
    x = []
    y = []
    for i in range(1, recent_years + 1):  # provide recent 6 month
        start_date = datetime(year=year, month=1, day=1)
        end_date = datetime(year=year, month=12, day=31, hour=23, minute=59, second=59)
        sum_energy = queryset.filter(dttfinishtime__gte=start_date, dttfinishtime__lt=end_date).aggregate(
            total=sum_zero('dblenergy'))['total']
        x.append(year)
        y.append(sum_energy)
        year = year - 1
    return dict(x=reversed(x), y=reversed(y))

def get_recent_days_list(days, step):
    """
    获取前N天的日期列表:['2019-06-07', '2019-06-08', '2019-06-09', '2019-06-10', '2019-06-11', '2019-06-12', '2019-06-13', '2019-06-14']
    days: 前days天
    step: 日间隔
    """
    date_list = []
    begin_date = date.today() + timedelta(-days)
    end_date = date.today()
    while begin_date <= end_date:
        date_list.append(begin_date.strftime("%Y-%m-%d"))
        begin_date += timedelta(days=step)
    return date_list

def get_recent_months_list(months, step):
    """
    获取前N个月的月份列表
    months: 月份(1-12)
    step: 月间隔,  例:get_recent_months_list(12, 3) return-->>['2018-6-14', '2018-9-14', '2018-12-14', '2019-3-14', '2019-6-14']
    """
    now = datetime.now()
    today_year = now.year
    today = now.day
    last_year =  int(now.year) -1
    if now.month+1 >= months:
        today_year_months = range(now.month+1-months, now.month+1, step)
        data_list_todays = []
        for today_year_month in today_year_months:
            data_list = '%s-%s-%s' % (last_year if today_year_month == 0 else today_year, 12 if today_year_month == 0 else today_year_month, today)
            data_list_todays.append(data_list)
        return data_list_todays

    today_year_months = range(0, now.month+1, step)
    last_year_months = range(12-(months-now.month), 12, step)
    data_list_lasts = []
    for last_year_month in last_year_months:
        date_list = '%s-%s-%s' % (last_year, 12 if last_year_month == 0 else last_year_month, today)
        data_list_lasts.append(date_list)

    data_list_todays = []
    for today_year_month in today_year_months:
        data_list = '%s-%s-%s' % (last_year if today_year_month == 0 else today_year, 12 if today_year_month == 0 else today_year_month, today)
        data_list_todays.append(data_list)

    data_year_month = data_list_lasts + data_list_todays
    return data_year_month

def get_recent_years_list(years, months, step):
    pass

def get_recent_charging_records(queryset, date_list):
    y = []
    n = []
    for i in range(1,len(date_list)):
        q = queryset.filter(dttstarttime__gte=datetime.strptime(date_list[i-1], "%Y-%m-%d"), 
                            dttstarttime__lt=datetime.strptime(date_list[i], "%Y-%m-%d"))
        sum_energy = q.aggregate(total=sum_zero('dblenergy'))['total']
        y.append(round(sum_energy,2))
        n.append(q.count())

    return dict(y=y, n=n)

def get_recent_charging_records2(queryset, date_list):
    y = []
    for i in range(1,len(date_list)):
        data = []
        q = queryset.filter(dttstarttime__gte=datetime.strptime(date_list[i-1], "%Y-%m-%d"), 
                            dttstarttime__lt=datetime.strptime(date_list[i], "%Y-%m-%d"))
        total = q.aggregate(sum_dblenergy=sum_zero('dblenergy'), sum_chargingtime=sum_zero(F('dttfinishtime') - F('dttstarttime')), 
                            sum_supplyvol=sum_zero('intsupplyvol'), sum_maxsupplycurrent=sum_zero('intmaxsupplycurrent'), n=Count("vchchargerid"))
        #maxphase   todo
        num = total["n"]
        if num > 0:
            data.append(date_list[i])                               #日期
            data.append(round(total["sum_dblenergy"],2))            #总电量
            data.append(int(total["sum_chargingtime"]/1000000))     #充电时间,秒
            data.append(round(total["sum_supplyvol"]/num, 2))       #平均电压
            data.append(3)                                          #相位取值待定  todo
            data.append(round(total["sum_maxsupplycurrent"]/num, 2))#平均电流
            data.append("20")                                       #故障记录
            data.append("test-----")                                #卡号(vchcardid)取值待定  todo
        y.append(data)
    return dict(y=y, n=num)
