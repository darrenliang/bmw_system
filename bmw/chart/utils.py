from datetime import datetime, timedelta
from share.db import sum_zero


# recent_days = 30
# recent_months = 12
# recent_years = 6


def get_daily_recent_charging_records(queryset, recent_days):
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    x = []
    y = []
    total = 0
    for i in range(1, recent_days + 1):  # provide recent 6 month
        start_date = datetime(year=year, month=month, day=day)
        end_date = datetime(year=year, month=month, day=day, hour=23, minute=59, second=59)
        sum_energy = queryset.filter(dttfinishtime__gte=start_date, dttfinishtime__lt=end_date).aggregate(
            total=sum_zero('dblenergy'))['total']

        dt = datetime.strptime("{0}-{1}-{2}".format(year, month, day), "%Y-%m-%d")
        x.append(dt.strftime("%Y-%m-%d"))
        y.append(sum_energy)
        total += sum_energy
        yesterday = start_date - timedelta(days=1)
        year = yesterday.year
        month = yesterday.month
        day = yesterday.day
    return dict(x=reversed(x), y=reversed(y), total=total)


def get_monthly_recent_charging_records(queryset, recent_months):
    now = datetime.now()
    year = now.year
    month = now.month
    x = []
    y = []
    total = 0
    for i in range(1, recent_months + 1):  # provide recent 6 month
        start_date = datetime(year=year, month=month, day=1)
        end_date = datetime(year=year if month < 12 else year + 1, month=month + 1 if month < 12 else 1, day=1)
        sum_energy = queryset.filter(dttfinishtime__gte=start_date, dttfinishtime__lt=end_date).aggregate(
            total=sum_zero('dblenergy'))['total']

        dt = datetime.strptime("{0}-{1}".format(year, month), "%Y-%m")
        x.append(dt.strftime("%Y-%m"))
        y.append(sum_energy)
        total += sum_energy
        month = month - 1 if month > 1 else 12
        year = year - 1 if month == 12 else year
    return dict(x=reversed(x), y=reversed(y), total=total)


def get_yearly_recent_charging_records(queryset, recent_years):
    now = datetime.now()
    year = now.year
    x = []
    y = []
    total = 0
    for i in range(1, recent_years + 1):  # provide recent 6 month
        start_date = datetime(year=year, month=1, day=1)
        end_date = datetime(year=year, month=12, day=31, hour=23, minute=59, second=59)
        sum_energy = queryset.filter(dttfinishtime__gte=start_date, dttfinishtime__lt=end_date).aggregate(
            total=sum_zero('dblenergy'))['total']
        x.append(year)
        y.append(sum_energy)
        total += sum_energy
        year = year - 1
    return dict(x=reversed(x), y=reversed(y), total=total)

