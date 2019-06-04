from rest_framework import serializers


class RecentChargingRecordSerial(serializers.Serializer):
    mode = serializers.IntegerField()
    vchchargerid = serializers.CharField(required=False)

