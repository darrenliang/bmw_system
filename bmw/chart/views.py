from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from . import utils
from ..meta import PeriodMode
from share.db import sum_zero
from bmw.models import ChargerInfo, ChargerState, ChargerModel, ChargingRecord, ChargerInfo, ChargerState, BasicSetting, \
    ChargerGroup
from rest_framework.exceptions import ValidationError


class RecentChargerRecordView(APIView):
    queryset = ChargingRecord.objects.all()
    serializer_class = serializers.RecentChargingRecordSerial

    def get(self, request):
        """
        SELECT sum(dblenergy) FROM evproject.charging_record where dttFinishTime
        between '2009-01-01' and '2009-02-01' and vchChargerID = ‘xxxxxxxx’;
        用如上示例SQL查询计算出前6个月每台电桩的充电量
        """
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)

        queryset = self.queryset
        if "vchchargerid" in serializer.validated_data:
            vchchargerid = serializer.validated_data["vchchargerid"]
            queryset = self.queryset.filter(vchchargerid=vchchargerid)

        mode = serializer.validated_data["mode"]
        if mode == PeriodMode.Yearly:
            data = utils.get_yearly_recent_charging_records(queryset)
        elif mode == PeriodMode.Monthly:
            data = utils.get_monthly_recent_charging_records(queryset)
        elif mode == PeriodMode.Daily:
            data = utils.get_daily_recent_charging_records(queryset)
        else:
            raise ValidationError("Wrong mode.{}!".format(mode))
        return Response(data)
