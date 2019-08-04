from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from . import utils
from ..meta import PeriodMode
from bmw.models import ChargingRecord, ChargerInfo
# from rest_framework.exceptions import ValidationError


class BaseChargerRecordView(APIView):
    queryset = ChargingRecord.objects.all()

    def get_charger_records(self, mode, offset, charger_id=None):
        queryset = self.queryset.filter(vchchargerid=charger_id) if charger_id else self.queryset
        if mode == PeriodMode.Yearly:
            return utils.get_yearly_recent_charging_records(queryset, offset)
        elif mode == PeriodMode.Monthly:
            return utils.get_monthly_recent_charging_records(queryset, offset)
        elif mode == PeriodMode.Daily:
            return utils.get_daily_recent_charging_records(queryset, offset)


class RecentChargerRecordView(BaseChargerRecordView):
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
        offset = serializer.validated_data["offset"]
        show_all = serializer.validated_data["show_all"]
        data = []
        for charger_id in [charger.vchchargerid for charger in ChargerInfo.objects.all()]:
            result = self.get_charger_records(mode=mode, offset=offset, charger_id=charger_id)

            if result is None:
                continue

            if show_all or (not show_all and result["total"] > 0):
                result["charger_id"] = charger_id
                data.append(result)

        return Response(data)


class AllRecentChargerRecordView(BaseChargerRecordView):
    serializer_class = serializers.AllRecentChargingRecordSerial

    def get(self, request):
        """
        SELECT sum(dblenergy) FROM evproject.charging_record where dttFinishTime
        between '2009-01-01' and '2009-02-01' and vchChargerID = ‘xxxxxxxx’;
        用如上示例SQL查询计算出前6个月每台电桩的充电量
        """
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        mode = serializer.validated_data["mode"]
        offset = serializer.validated_data["offset"]
        charger_id = serializer.validated_data["charger_id"] if "charger_id" in serializer.validated_data else None
        result = self.get_charger_records(mode=mode, offset=offset, charger_id=charger_id)
        return Response(result)
