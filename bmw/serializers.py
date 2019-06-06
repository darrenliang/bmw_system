from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChargerGroup, ChargerInfo, ChargerState


class ChargerGroupSerializer(serializers.ModelSerializer):
    vchgroupid = serializers.CharField()

    class Meta:
        model = ChargerGroup
        fields = ('vchgroupid', )


class ChargerInfoSerializer(serializers.ModelSerializer):
    vchchargerid = serializers.CharField()
    vchgroupid = serializers.CharField()
    vchfirmwarever = serializers.CharField()
    vchmodelid = serializers.CharField()

    #
    # vchchargerid = models.CharField(db_column='vchChargerID', primary_key=True, max_length=11)  # Field name made lowercase.
    # vchvenderid = models.CharField(db_column='vchVenderID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    # vchgrouptransformer = models.CharField(db_column='vchGroupTransformer', max_length=10)  # Field name made lowercase.
    # vchmodelid = models.CharField(db_column='vchModelID', max_length=30)  # Field name made lowercase.
    # vchgroupid = models.CharField(db_column='vchGroupID', max_length=8)  # Field name made lowercase.
    # vchserialno = models.CharField(db_column='vchSerialNo', max_length=30)  # Field name made lowercase.
    # vchfirmwarever = models.CharField(db_column='vchFirmwareVer', max_length=25)  # Field name made lowercase.
    # datmanufacturingdate = models.DateField(db_column='datManufacturingDate')  # Field name made lowercase.
    # dblaccumlatedpower = models.FloatField(db_column='dblAccumlatedPower')  # Field name made lowercase.
    # dblaccumlatedminute = models.FloatField(db_column='dblAccumlatedMinute')  # Field name made lowercase.
    # vchprotocol = models.FloatField(db_column='vchProtocol', blank=True, null=True)  # Field name made lowercase.
    # vchip = models.CharField(db_column='vchIP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    # vchmac = models.CharField(db_column='vchMAC', max_length=20, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        model = ChargerInfo
        fields = ('vchgroupid', )


class ChargerStateSerializer(serializers.ModelSerializer):
    vchchargerid = serializers.CharField()
    vchstate = serializers.CharField()

    class Meta:
        model = ChargerState
        fields = ('vchchargerid', 'vchstate')


class UserWithoutUsernameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',)
        
    '''
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'snippets',)
        
        extra_kwargs = {
            'password': {'write_only': True},
        }
    '''  
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

