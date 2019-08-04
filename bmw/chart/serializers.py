from rest_framework import serializers


class RecentChargingRecordSerial(serializers.Serializer):
    mode = serializers.IntegerField()
    offset = serializers.IntegerField(default=7)
    show_all = serializers.BooleanField(default=False)


class AllRecentChargingRecordSerial(serializers.Serializer):
    mode = serializers.IntegerField()
    charger_id = serializers.CharField(required=False)
    offset = serializers.IntegerField(default=7)

