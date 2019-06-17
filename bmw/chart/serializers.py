from rest_framework import serializers


class RecentChargingRecordSerial(serializers.Serializer):
    mode = serializers.IntegerField()


class AllRecentChargingRecordSerial(serializers.Serializer):
    charger_id = serializers.CharField(required=False)
    mode = serializers.IntegerField()

class GetChargingRecordBarSerial(serializers.Serializer):
    group_id = serializers.CharField()
    mode = serializers.IntegerField()

class GetChargersErrLogSunSerial(serializers.Serializer):
    group_id = serializers.CharField()

class GetChargingRecordScatterSerial(serializers.Serializer):
    group_id = serializers.CharField()
    mode = serializers.IntegerField()