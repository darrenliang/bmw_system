from datetime import datetime
from share.db import sum_zero


def get_monthly_recent_charging_records(queryset):
    recent_months = 6
    now = datetime.now()
    year = now.year
    month = now.month
    year = 2015
    month = 12
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
