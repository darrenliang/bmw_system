from rest_framework import serializers
from bmw.models import ChargingRecord


class RecentChargingRecordSerial(serializers.Serializer):
    vchchargerid = serializers.CharField(required=False)

