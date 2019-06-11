from rest_framework import serializers


class RecentChargingRecordSerial(serializers.Serializer):
    mode = serializers.IntegerField()


class AllRecentChargingRecordSerial(serializers.Serializer):
    charger_id = serializers.CharField(required=False)
    mode = serializers.IntegerField()

