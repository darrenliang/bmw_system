from share.meta import get_sth_display


class PeriodMode:
    Yearly = 1
    Monthly = 2
    Daily = 3

    Days_7 = 11
    Weeks_7 = 12
    Quarter_4 = 13
    Days_30 = 14
    Months_6 = 15
    Months_12 = 16


STATES = ["BootUp", "Available", "PreParing", "Charging", "StatusChanged", "StopCharging",
          "RemoteCharging", "RemoteStopCharging", "SendMessage", "Updating", "Unavailable", "Reboot",
          "Faulted", "SupsendedEV", "Finishing", "Other"]


parking_floor_tuple = (("05010101", 19), ("05010102", 20), ("05010103", 21), ("05010104", 22),
                       ("05010105", 23), ("05010106", 24), ("05010107", 25), ("05010108", 26),
                       ("05010109", 27), ("05010110", 28), ("05010201", 45), ("05010202", 44),
                       ("05010203", 43), ("05010204", 42), ("05010205", 41), ("05010206", 40),
                       ("05010207", 39), ("05010208", 38), ("05010209", 37), ("05010210", 36))

errTypeList = ["待机中CP错误", "充电中CP错误", "cc未检测到", "电表故障", "温度过高", "交流电故障"]

def get_parking_floor_display(charger_id):
    return get_sth_display(charger_id, choices=parking_floor_tuple)


