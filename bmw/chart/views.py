from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from . import utils
from ..meta import PeriodMode
from bmw.models import ChargingRecord, ChargerInfo
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
        mode = serializer.validated_data["mode"]
        data = []
        for charger_id in [charger.vchchargerid for charger in ChargerInfo.objects.all()]:
            result = None
            queryset = self.queryset.filter(vchchargerid=charger_id)
            if mode == PeriodMode.Yearly:
                result = utils.get_yearly_recent_charging_records(queryset)
            elif mode == PeriodMode.Monthly:
                result = utils.get_monthly_recent_charging_records(queryset)
            elif mode == PeriodMode.Daily:
                result = utils.get_daily_recent_charging_records(queryset)

            if result:
                x = list(result["x"])
                y = list(result["y"])
                if len(x) > 0 and len(y) > 0 and sum(y) > 0:
                    data.append(dict(charger_id=charger_id, x=x, y=y))
        return Response(data)


class AllRecentChargerRecordView(APIView):
    queryset = ChargingRecord.objects.all()
    serializer_class = serializers.AllRecentChargingRecordSerial

    def get(self, request):
        """
        SELECT sum(dblenergy) FROM evproject.charging_record where dttFinishTime
        between '2009-01-01' and '2009-02-01' and vchChargerID = ‘xxxxxxxx’;
        用如上示例SQL查询计算出前6个月每台电桩的充电量
        """
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)

        queryset = self.queryset
        if "charger_id" in serializer.validated_data:
            charger_id = serializer.validated_data["charger_id"]
            queryset = self.queryset.filter(vchchargerid=charger_id)

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
