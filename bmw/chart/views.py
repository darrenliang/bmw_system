from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from . import utils
from ..meta import PeriodMode, errTypeList
from bmw.models import ChargingRecord, ChargerInfo, ChargerErrorLog
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


class GetChargingRecordBarView(APIView):
    queryset = ChargerInfo.objects.all()
    serializer_class = serializers.GetChargingRecordBarSerial

    def get(self, request):
        """
        电桩充电记录条形图
        """
        charger_list = []
        total_y = []
        charging_num = []
        date_list = []
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        
        queryset = self.queryset
        if "group_id" in serializer.validated_data:
            group_id = serializer.validated_data["group_id"]
            queryset = self.queryset.filter(vchgroupid=group_id)

        mode = serializer.validated_data["mode"]
        if mode == PeriodMode.Days_7 or mode == PeriodMode.Weeks_7:     #初始化列表为0
            total_y = charging_num = [0] * 7
        else:
            total_y = charging_num = [0] * 4

        for charger_id in queryset.values_list("vchchargerid", flat=True):
            result = None
            queryset = ChargingRecord.objects.filter(vchchargerid=charger_id)
            if mode == PeriodMode.Days_7:
                date_list=utils.get_recent_days_list(7, 1)
            elif mode == PeriodMode.Weeks_7:
                date_list=utils.get_recent_days_list(49, 7)
            elif mode == PeriodMode.Quarter_4:
                date_list=utils.get_recent_months_list(12, 3)

            result = utils.get_recent_charging_records(queryset, date_list)
            if result:
                y = list(result["y"])
                n = list(result["n"])
                charger_list.append(dict(charger_id=charger_id, y=y))
                total_y = [y[i]+total_y[i] for i in range(0,len(y))]        #每个电桩y对应项求和
                charging_num = [n[i]+charging_num[i] for i in range(0,len(n))]    #每个电桩充电次数对应项求和

        del(date_list[0])   #第一个时间点仅供查询数据库使用，web页面不需要
        dic = {
            'charger_list':charger_list,
            'total_y':total_y,
            'charging_num':charging_num,
            'date_list':date_list
        }
        return Response(dic)

class GetChargersErrLogSunView(APIView):
    serializer_class = serializers.GetChargersErrLogSunSerial
    def get_second_children_dic(self, cid, errType):
        """
        获取二级children参数
        """
        list = []
        queryset = ChargerErrorLog.objects.filter(vchchargerid=cid,interror=errType+1)
        for i in queryset:
            tmp = {
                "name": i.dtterrortime.strftime("%Y-%m-%d"),
                "value": 1,
                "itemStyle": {"color": "#f99e1c"}
            }
            list.append(tmp)
        dic = {
            "name": errTypeList[errType],
            "itemStyle": {"color": "#f44336"},
            "children": list
        }
        return dic

    def get(self, request):
        """
        电桩错误日志旭日图参数
        """
        data = []
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        if "group_id" in serializer.validated_data:
            group_id = serializer.validated_data["group_id"]

        #testList = ["05010101","05010102"]
        queryset = ChargerInfo.objects.filter(vchgroupid=group_id)
        for charger_id in queryset.values_list("vchchargerid", flat=True):
        #for charger_id in testList:
            charger_first_list = []
            for index in range(len(errTypeList)):
                charger_first_list.append(self.get_second_children_dic(charger_id, index))

            dic = {
                "name": charger_id,
                "itemStyle": {"color": "#009688"},
                "children": charger_first_list
            }

            data.append(dic)
        return Response(data)

class GetChargingQuantityLineView(APIView):
    def get(self, request):
        return Response(None)
    
class GetChargingRecordScatterView(APIView):
    queryset = ChargerInfo.objects.all()
    serializer_class = serializers.GetChargingRecordScatterSerial

    def get(self, request):
        """
        电桩充电记录散点图
        """
        charger_list = []
        date_list = []
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        queryset = self.queryset
        if "group_id" in serializer.validated_data:
            group_id = serializer.validated_data["group_id"]
            queryset = self.queryset.filter(vchgroupid=group_id)
        
        mode = serializer.validated_data["mode"]
        
        for charger_id in queryset.values_list("vchchargerid", flat=True):
            result = None
            queryset = ChargingRecord.objects.filter(vchchargerid=charger_id)
            if mode == PeriodMode.Days_30:
                date_list=utils.get_recent_days_list(30, 1)
            elif mode == PeriodMode.Months_6:
                date_list=utils.get_recent_months_list(6, 1)
            elif mode == PeriodMode.Months_12:
                date_list=utils.get_recent_months_list(12, 1)
            result = utils.get_recent_charging_records2(queryset, date_list)
            if result:
                y = list(result["y"])
                charger_list.append(dict(charger_id=charger_id, y=y))

        del(date_list[0])   #第一个时间点仅供查询数据库使用，web页面不需要
        dic = {
            'charger_list':charger_list,
            'date_list':date_list
        }
        #print(charger_list)
        return Response(dic)