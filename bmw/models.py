from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class BasicSetting(models.Model):
    vchcardreadercom = models.CharField(db_column='vchCardReaderCom', primary_key=True, max_length=10)  # Field name made lowercase.
    yeainstallyear = models.TextField(db_column='yeaInstallYear')  # Field name made lowercase. This field type is a guess.
    intinstallmonth = models.IntegerField(db_column='intInstallMonth')  # Field name made lowercase.
    blncurrentdistribution = models.IntegerField(db_column='blnCurrentDistribution')  # Field name made lowercase.
    vchpowermetercom = models.CharField(db_column='vchPowerMeterCom', max_length=10)  # Field name made lowercase.
    vchpowersequence = models.CharField(db_column='vchPowerSequence', max_length=10)  # Field name made lowercase.
    intcurrency = models.IntegerField(db_column='intCurrency')  # Field name made lowercase.
    dblchargingdeductionpower = models.FloatField(db_column='dblChargingDeductionPower')  # Field name made lowercase.
    intchargingdeductionminute = models.IntegerField(db_column='intChargingDeductionMinute')  # Field name made lowercase.
    intdeductionprioritypower = models.IntegerField(db_column='intDeductionPriorityPower')  # Field name made lowercase.
    intdeductionpriorityminute = models.IntegerField(db_column='intDeductionPriorityMinute')  # Field name made lowercase.
    dblpowercoefficient = models.FloatField(db_column='dblPowerCoefficient')  # Field name made lowercase.
    blninternaltesting = models.IntegerField(db_column='blnInternalTesting')  # Field name made lowercase.
    intmaxcurrenta = models.IntegerField(db_column='intMaxCurrentA')  # Field name made lowercase.
    intmaxcurrentb = models.IntegerField(db_column='intMaxCurrentB')  # Field name made lowercase.
    intmaxcurrentc = models.IntegerField(db_column='intMaxCurrentC')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'basic_setting'
        unique_together = (('vchcardreadercom', 'yeainstallyear', 'intinstallmonth', 'blncurrentdistribution', 'vchpowermetercom', 'vchpowersequence', 'intcurrency', 'dblchargingdeductionpower', 'intchargingdeductionminute', 'intdeductionprioritypower', 'intdeductionpriorityminute', 'dblpowercoefficient', 'blninternaltesting'),)


class ChargerCost(models.Model):
    vchsocketid = models.ForeignKey('SocketType', models.DO_NOTHING, db_column='vchSocketID', primary_key=True)  # Field name made lowercase.
    blnmonthly = models.IntegerField(db_column='blnMonthly')  # Field name made lowercase.
    flthr00_01 = models.FloatField(db_column='fltHr00_01')  # Field name made lowercase.
    flthr01_02 = models.FloatField(db_column='fltHr01_02')  # Field name made lowercase.
    flthr02_03 = models.FloatField(db_column='fltHr02_03')  # Field name made lowercase.
    flthr03_04 = models.FloatField(db_column='fltHr03_04')  # Field name made lowercase.
    flthr04_05 = models.FloatField(db_column='fltHr04_05')  # Field name made lowercase.
    flthr05_06 = models.FloatField(db_column='fltHr05_06')  # Field name made lowercase.
    flthr06_07 = models.FloatField(db_column='fltHr06_07')  # Field name made lowercase.
    flthr07_08 = models.FloatField(db_column='fltHr07_08')  # Field name made lowercase.
    flthr08_09 = models.FloatField(db_column='fltHr08_09')  # Field name made lowercase.
    flthr09_10 = models.FloatField(db_column='fltHr09_10')  # Field name made lowercase.
    flthr10_11 = models.FloatField(db_column='fltHr10_11')  # Field name made lowercase.
    flthr11_12 = models.FloatField(db_column='fltHr11_12')  # Field name made lowercase.
    flthr12_13 = models.FloatField(db_column='fltHr12_13')  # Field name made lowercase.
    flthr13_14 = models.FloatField(db_column='fltHr13_14')  # Field name made lowercase.
    flthr14_15 = models.FloatField(db_column='fltHr14_15')  # Field name made lowercase.
    flthr15_16 = models.FloatField(db_column='fltHr15_16')  # Field name made lowercase.
    flthr16_17 = models.FloatField(db_column='fltHr16_17')  # Field name made lowercase.
    flthr17_18 = models.FloatField(db_column='fltHr17_18')  # Field name made lowercase.
    flthr18_19 = models.FloatField(db_column='fltHr18_19')  # Field name made lowercase.
    flthr19_20 = models.FloatField(db_column='fltHr19_20')  # Field name made lowercase.
    flthr20_21 = models.FloatField(db_column='fltHr20_21')  # Field name made lowercase.
    flthr21_22 = models.FloatField(db_column='fltHr21_22')  # Field name made lowercase.
    flthr22_23 = models.FloatField(db_column='fltHr22_23')  # Field name made lowercase.
    flthr23_00 = models.FloatField(db_column='fltHr23_00')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_cost'
        unique_together = (('vchsocketid', 'blnmonthly'),)


class ChargerCostChange(models.Model):
    vchgroupid = models.CharField(db_column='vchGroupID', primary_key=True, max_length=8)  # Field name made lowercase.
    vchsocketid = models.CharField(db_column='vchSocketID', max_length=15)  # Field name made lowercase.
    dttupdatetime = models.DateTimeField(db_column='dttUpdateTime')  # Field name made lowercase.
    flthr00_01 = models.FloatField(db_column='fltHr00_01')  # Field name made lowercase.
    flthr01_02 = models.FloatField(db_column='fltHr01_02')  # Field name made lowercase.
    flthr02_03 = models.FloatField(db_column='fltHr02_03')  # Field name made lowercase.
    flthr03_04 = models.FloatField(db_column='fltHr03_04')  # Field name made lowercase.
    flthr04_05 = models.FloatField(db_column='fltHr04_05')  # Field name made lowercase.
    flthr05_06 = models.FloatField(db_column='fltHr05_06')  # Field name made lowercase.
    flthr06_07 = models.FloatField(db_column='fltHr06_07')  # Field name made lowercase.
    flthr07_08 = models.FloatField(db_column='fltHr07_08')  # Field name made lowercase.
    flthr08_09 = models.FloatField(db_column='fltHr08_09')  # Field name made lowercase.
    flthr09_10 = models.FloatField(db_column='fltHr09_10')  # Field name made lowercase.
    flthr10_11 = models.FloatField(db_column='fltHr10_11')  # Field name made lowercase.
    flthr11_12 = models.FloatField(db_column='fltHr11_12')  # Field name made lowercase.
    flthr12_13 = models.FloatField(db_column='fltHr12_13')  # Field name made lowercase.
    flthr13_14 = models.FloatField(db_column='fltHr13_14')  # Field name made lowercase.
    flthr14_15 = models.FloatField(db_column='fltHr14_15')  # Field name made lowercase.
    flthr15_16 = models.FloatField(db_column='fltHr15_16')  # Field name made lowercase.
    flthr16_17 = models.FloatField(db_column='fltHr16_17')  # Field name made lowercase.
    flthr17_18 = models.FloatField(db_column='fltHr17_18')  # Field name made lowercase.
    flthr18_19 = models.FloatField(db_column='fltHr18_19')  # Field name made lowercase.
    flthr19_20 = models.FloatField(db_column='fltHr19_20')  # Field name made lowercase.
    flthr20_21 = models.FloatField(db_column='fltHr20_21')  # Field name made lowercase.
    flthr21_22 = models.FloatField(db_column='fltHr21_22')  # Field name made lowercase.
    flthr22_23 = models.FloatField(db_column='fltHr22_23')  # Field name made lowercase.
    flthr23_00 = models.FloatField(db_column='fltHr23_00')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_cost_change'
        unique_together = (('vchgroupid', 'vchsocketid'),)


class ChargerCurrent(models.Model):
    vchchargerid = models.ForeignKey('ChargerInfo', models.DO_NOTHING, db_column='vchChargerID', primary_key=True)  # Field name made lowercase.
    vchsocketid = models.ForeignKey('SocketType', models.DO_NOTHING, db_column='vchSocketID')  # Field name made lowercase.
    intphase = models.IntegerField(db_column='intPhase')  # Field name made lowercase.
    intcurrent = models.IntegerField(db_column='intCurrent')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_current'
        unique_together = (('vchchargerid', 'vchsocketid'),)


class ChargerErrorLog(models.Model):
    interrorid = models.AutoField(db_column='intErrorID', primary_key=True)  # Field name made lowercase.
    vchchargerid = models.CharField(db_column='vchChargerID', max_length=11)  # Field name made lowercase.
    interror = models.IntegerField(db_column='intError')  # Field name made lowercase.
    dtterrortime = models.DateTimeField(db_column='dttErrorTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_error_log'


class ChargerGroup(models.Model):
    vchgroupid = models.CharField(db_column='vchGroupID', primary_key=True, max_length=8)  # Field name made lowercase.
    vchownerid = models.CharField(db_column='vchOwnerID', max_length=5)  # Field name made lowercase.
    vchmanagementid = models.CharField(db_column='vchManagementID', max_length=5)  # Field name made lowercase.
    vchstaffid = models.CharField(db_column='vchStaffID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    dbllocationx = models.FloatField(db_column='dblLocationX')  # Field name made lowercase.
    dbllocationy = models.FloatField(db_column='dblLocationY')  # Field name made lowercase.
    blnopenpublic = models.IntegerField(db_column='blnOpenPublic')  # Field name made lowercase.
    blnconnectserver = models.IntegerField(db_column='blnConnectServer')  # Field name made lowercase.
    datinstalldate = models.DateField(db_column='datInstallDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_group'


class ChargerInfo(models.Model):
    vchchargerid = models.CharField(db_column='vchChargerID', primary_key=True, max_length=11)  # Field name made lowercase.
    vchvenderid = models.CharField(db_column='vchVenderID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    vchgrouptransformer = models.CharField(db_column='vchGroupTransformer', max_length=10)  # Field name made lowercase.
    vchmodelid = models.CharField(db_column='vchModelID', max_length=30)  # Field name made lowercase.
    vchgroupid = models.CharField(db_column='vchGroupID', max_length=8)  # Field name made lowercase.
    vchserialno = models.CharField(db_column='vchSerialNo', max_length=30)  # Field name made lowercase.
    vchfirmwarever = models.CharField(db_column='vchFirmwareVer', max_length=25)  # Field name made lowercase.
    datmanufacturingdate = models.DateField(db_column='datManufacturingDate')  # Field name made lowercase.
    dblaccumlatedpower = models.FloatField(db_column='dblAccumlatedPower')  # Field name made lowercase.
    dblaccumlatedminute = models.FloatField(db_column='dblAccumlatedMinute')  # Field name made lowercase.
    vchprotocol = models.FloatField(db_column='vchProtocol', blank=True, null=True)  # Field name made lowercase.
    vchip = models.CharField(db_column='vchIP', max_length=20, blank=True, null=True)  # Field name made lowercase.
    vchmac = models.CharField(db_column='vchMAC', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_info'


class ChargerInstall(models.Model):
    vchchargerid = models.ForeignKey(ChargerInfo, models.DO_NOTHING, db_column='vchChargerID', primary_key=True)  # Field name made lowercase.
    vchspot = models.CharField(db_column='vchSpot', max_length=10)  # Field name made lowercase.
    vchfloor = models.CharField(db_column='vchFloor', max_length=10)  # Field name made lowercase.
    blnopenpublic = models.IntegerField(db_column='blnOpenPublic')  # Field name made lowercase.
    blnreservable = models.IntegerField(db_column='blnReservable')  # Field name made lowercase.
    blnoperatedbymanagement = models.IntegerField(db_column='blnOperatedByManagement')  # Field name made lowercase.
    blnparkingsenser = models.IntegerField(db_column='blnParkingSenser')  # Field name made lowercase.
    blnparkingsensor = models.IntegerField(db_column='blnParkingSensor')  # Field name made lowercase.
    blnparkingsensorparkhigh = models.IntegerField(db_column='blnParkingSensorParkHigh')  # Field name made lowercase.
    intchargingshareratio = models.IntegerField(db_column='intChargingShareRatio')  # Field name made lowercase.
    intmemberchargingshareratio = models.IntegerField(db_column='intMemberChargingShareRatio')  # Field name made lowercase.
    intreserveshareratio = models.IntegerField(db_column='intReserveShareRatio')  # Field name made lowercase.
    datinstallationdate = models.DateField(db_column='datInstallationDate')  # Field name made lowercase.
    intsafecurrent = models.IntegerField(db_column='intSafeCurrent')  # Field name made lowercase.
    intupdatecomment = models.IntegerField(db_column='intUpdateComment')  # Field name made lowercase.
    datmaintenanceduedate = models.DateField(db_column='datMaintenanceDueDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_install'


class ChargerLock(models.Model):
    vchchargerid = models.CharField(db_column='vchChargerID', primary_key=True, max_length=11)  # Field name made lowercase.
    vchlockcode = models.CharField(db_column='vchLockCode', max_length=10)  # Field name made lowercase.
    dttlockendtime = models.DateTimeField(db_column='dttLockEndTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_lock'


class ChargerModel(models.Model):
    vchmodelid = models.CharField(db_column='vchModelID', primary_key=True, max_length=30)  # Field name made lowercase.
    vchbrand = models.CharField(db_column='vchBrand', max_length=50)  # Field name made lowercase.
    vchmodel = models.CharField(db_column='vchModel', max_length=20)  # Field name made lowercase.
    vchcmsmode = models.CharField(db_column='vchCMSMode', max_length=10)  # Field name made lowercase.
    dblmaxpower = models.FloatField(db_column='dblMaxPower')  # Field name made lowercase.
    dblmaxcurrent = models.FloatField(db_column='dblMaxCurrent')  # Field name made lowercase.
    dblmincurrent = models.FloatField(db_column='dblMinCurrent')  # Field name made lowercase.
    intmaxphase = models.IntegerField(db_column='intMaxPhase')  # Field name made lowercase.
    vchdescription = models.CharField(db_column='vchDescription', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_model'


class ChargerSocket(models.Model):
    vchmodelid = models.ForeignKey(ChargerModel, models.DO_NOTHING, db_column='vchModelID', primary_key=True)  # Field name made lowercase.
    vchsocketid = models.CharField(db_column='vchSocketID', max_length=15)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_socket'
        unique_together = (('vchmodelid', 'vchsocketid'),)


class ChargerState(models.Model):
    vchchargerid = models.CharField(db_column='vchChargerID', primary_key=True, max_length=11)  # Field name made lowercase.
    intreserverecordid = models.IntegerField(db_column='intReserveRecordID', blank=True, null=True)  # Field name made lowercase.
    intchargingrecordid = models.IntegerField(db_column='intChargingRecordID', blank=True, null=True)  # Field name made lowercase.
    intprechargerecordid = models.IntegerField(db_column='intPrechargeRecordID', blank=True, null=True)  # Field name made lowercase.
    intsystemmessage = models.IntegerField(db_column='intSystemMessage', blank=True, null=True)  # Field name made lowercase.
    vchstate = models.CharField(db_column='vchState', max_length=40)  # Field name made lowercase.
    vchfeedbackstate = models.CharField(db_column='vchFeedbackState', max_length=40)  # Field name made lowercase.
    vchsocket = models.CharField(db_column='vchSocket', max_length=20)  # Field name made lowercase.
    intcurrent = models.IntegerField(db_column='intCurrent')  # Field name made lowercase.
    intcurrentfeedback = models.IntegerField(db_column='intCurrentFeedback')  # Field name made lowercase.
    blnmanual = models.IntegerField(db_column='blnManual')  # Field name made lowercase.
    blnsae_plugged = models.IntegerField(db_column='blnSAE_Plugged')  # Field name made lowercase.
    blnsae_ready = models.IntegerField(db_column='blnSAE_Ready')  # Field name made lowercase.
    blnsae_complete = models.IntegerField(db_column='blnSAE_Complete')  # Field name made lowercase.
    blniecgb_plugged = models.IntegerField(db_column='blnIECGB_Plugged')  # Field name made lowercase.
    blniecgb_complete = models.IntegerField(db_column='blnIECGB_Complete')  # Field name made lowercase.
    blniecgb_ready = models.IntegerField(db_column='blnIECGB_Ready')  # Field name made lowercase.
    blniecgb_13a = models.IntegerField(db_column='blnIECGB_13A')  # Field name made lowercase.
    blniecgb_16a = models.IntegerField(db_column='blnIECGB_16A')  # Field name made lowercase.
    blniecgb_20a = models.IntegerField(db_column='blnIECGB_20A')  # Field name made lowercase.
    blniecgb_32a = models.IntegerField(db_column='blnIECGB_32A')  # Field name made lowercase.
    blniecgb_63a = models.IntegerField(db_column='blnIECGB_63A')  # Field name made lowercase.
    vchupdatecommand = models.CharField(db_column='vchUpdateCommand', max_length=50)  # Field name made lowercase.
    intchargingcurrent = models.IntegerField(db_column='intChargingCurrent')  # Field name made lowercase.
    intconsumedenergy = models.IntegerField(db_column='intConsumedEnergy')  # Field name made lowercase.
    intelapsedtime = models.IntegerField(db_column='intElapsedTime')  # Field name made lowercase.
    intchargingphase = models.IntegerField(db_column='intChargingPhase')  # Field name made lowercase.
    vchcommand = models.CharField(db_column='vchCommand', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_state'


class ChargerStateLog(models.Model):
    intlogid = models.AutoField(db_column='intLogID', primary_key=True)  # Field name made lowercase.
    vchchargerid = models.CharField(db_column='vchChargerID', max_length=11)  # Field name made lowercase.
    vchpreviousstate = models.CharField(db_column='vchPreviousState', max_length=2)  # Field name made lowercase.
    vchpresentstate = models.CharField(db_column='vchPresentState', max_length=2)  # Field name made lowercase.
    dttdate = models.DateTimeField(db_column='dttDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charger_state_log'


class ChargingCard(models.Model):
    vchcardid = models.CharField(db_column='vchCardID', primary_key=True, max_length=15)  # Field name made lowercase.
    vchprivateid = models.CharField(db_column='vchPrivateID', unique=True, max_length=50)  # Field name made lowercase.
    dttactivationdate = models.DateTimeField(db_column='dttActivationDate')  # Field name made lowercase.
    dttexpirydate = models.DateTimeField(db_column='dttExpiryDate', blank=True, null=True)  # Field name made lowercase.
    dttlastusage = models.DateTimeField(db_column='dttLastUsage')  # Field name made lowercase.
    vchrole = models.CharField(db_column='vchRole', max_length=10)  # Field name made lowercase.
    intchargingminute = models.IntegerField(db_column='intChargingMinute', blank=True, null=True)  # Field name made lowercase.
    dblvalue = models.FloatField(db_column='dblValue')  # Field name made lowercase.
    vchremark = models.CharField(db_column='vchRemark', max_length=30)  # Field name made lowercase.
    blndefault = models.IntegerField(db_column='blnDefault')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charging_card'


class ChargingRecord(models.Model):
    intrecordid = models.AutoField(db_column='intRecordID', primary_key=True)  # Field name made lowercase.
    intchargingcode = models.IntegerField(db_column='intChargingCode')  # Field name made lowercase.
    vchchargerid = models.CharField(db_column='vchChargerID', max_length=11)  # Field name made lowercase.
    vchcardid = models.CharField(db_column='vchCardID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    vchsocketid = models.ForeignKey('SocketType', models.DO_NOTHING, db_column='vchSocketID')  # Field name made lowercase.
    vchrecordstate = models.CharField(db_column='vchRecordState', max_length=10)  # Field name made lowercase.
    vchopenrecord = models.CharField(db_column='vchOpenRecord', max_length=30)  # Field name made lowercase.
    vchcloserecord = models.CharField(db_column='vchCloseRecord', max_length=30)  # Field name made lowercase.
    blnmonthly = models.IntegerField(db_column='blnMonthly')  # Field name made lowercase.
    vchpriority = models.CharField(db_column='vchPriority', max_length=15)  # Field name made lowercase.
    intchargingminute = models.IntegerField(db_column='intChargingMinute')  # Field name made lowercase.
    intdelayminute = models.IntegerField(db_column='intDelayMinute')  # Field name made lowercase.
    dblenergy = models.FloatField(db_column='dblEnergy')  # Field name made lowercase.
    blncurrentmaxcomplete = models.IntegerField(db_column='blnCurrentMaxComplete')  # Field name made lowercase.
    blncurrentmincomplete = models.IntegerField(db_column='blnCurrentMinComplete')  # Field name made lowercase.
    blncurrentsafecomplete = models.IntegerField(db_column='blnCurrentSafeComplete')  # Field name made lowercase.
    vchsupplyline = models.CharField(db_column='vchSupplyLine', max_length=3, blank=True, null=True)  # Field name made lowercase.
    intmaxsupplycurrent = models.IntegerField(db_column='intMaxSupplyCurrent')  # Field name made lowercase.
    intmaxcurrent = models.IntegerField(db_column='intMaxCurrent')  # Field name made lowercase.
    intmincurrent = models.IntegerField(db_column='intMinCurrent')  # Field name made lowercase.
    intsafecurrent = models.IntegerField(db_column='intSafeCurrent')  # Field name made lowercase.
    intsupplycurrenttocharger = models.IntegerField(db_column='intSupplyCurrentToCharger')  # Field name made lowercase.
    intpwnchangedelay = models.IntegerField(db_column='intPWNChangeDelay')  # Field name made lowercase.
    dttstartqueue = models.DateTimeField(db_column='dttStartQueue')  # Field name made lowercase.
    dttstarttime = models.DateTimeField(db_column='dttStartTime', blank=True, null=True)  # Field name made lowercase.
    dttfinishtime = models.DateTimeField(db_column='dttFinishTime', blank=True, null=True)  # Field name made lowercase.
    dttrealfinish = models.DateTimeField(db_column='dttRealFinish', blank=True, null=True)  # Field name made lowercase.
    dttlockuntil = models.DateTimeField(db_column='dttLockUntil', blank=True, null=True)  # Field name made lowercase.
    dblcost = models.FloatField(db_column='dblCost')  # Field name made lowercase.
    vchremark = models.CharField(db_column='vchRemark', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'charging_record'


class GroupCurrent(models.Model):
    vchgrouptransformer = models.CharField(db_column='vchGroupTransformer', primary_key=True, max_length=10)  # Field name made lowercase.
    vchgroupid = models.ForeignKey(ChargerGroup, models.DO_NOTHING, db_column='vchGroupID')  # Field name made lowercase.
    transformerdescription = models.CharField(db_column='TransformerDescription', max_length=30, blank=True, null=True)  # Field name made lowercase.
    intcurrentr = models.IntegerField(db_column='intCurrentR')  # Field name made lowercase.
    intcurrents = models.IntegerField(db_column='intCurrentS')  # Field name made lowercase.
    intcurrentt = models.IntegerField(db_column='intCurrentT')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'group_current'


class Message(models.Model):
    intmessageid = models.AutoField(db_column='intMessageID', primary_key=True)  # Field name made lowercase.
    vchchargerid = models.CharField(db_column='vchChargerID', max_length=10)  # Field name made lowercase.
    intmessage = models.IntegerField(db_column='intMessage')  # Field name made lowercase.
    dttdate = models.DateTimeField(db_column='dttDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'message'


class PrechargeRecord(models.Model):
    intrecordid = models.AutoField(db_column='intRecordID', primary_key=True)  # Field name made lowercase.
    vchchargerid = models.CharField(db_column='vchChargerID', max_length=11)  # Field name made lowercase.
    vchrecordstate = models.CharField(db_column='vchRecordState', max_length=10)  # Field name made lowercase.
    dttstarttime = models.DateTimeField(db_column='dttStartTime')  # Field name made lowercase.
    dttfinishtime = models.DateTimeField(db_column='dttFinishTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'precharge_record'


class ReserveRecord(models.Model):
    intrecordid = models.AutoField(db_column='intRecordID', primary_key=True)  # Field name made lowercase.
    vchchargerid = models.CharField(db_column='vchChargerID', max_length=11)  # Field name made lowercase.
    vchcardid = models.CharField(db_column='vchCardID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    vchrecordstate = models.CharField(db_column='vchRecordState', max_length=20)  # Field name made lowercase.
    dttstarttime = models.DateTimeField(db_column='dttStartTime')  # Field name made lowercase.
    dttfinishtime = models.DateTimeField(db_column='dttFinishTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reserve_record'


class SocketType(models.Model):
    vchsocketid = models.CharField(db_column='vchSocketID', primary_key=True, max_length=15)  # Field name made lowercase.
    vchsocket = models.CharField(db_column='vchSocket', max_length=15)  # Field name made lowercase.
    intsocketcode = models.IntegerField(db_column='intSocketCode', blank=True, null=True)  # Field name made lowercase.
    vchsocketshortform = models.CharField(db_column='vchSocketShortForm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    intlevel = models.IntegerField(db_column='intLevel')  # Field name made lowercase.
    intsupplycurrent = models.IntegerField(db_column='intSupplyCurrent')  # Field name made lowercase.
    intphase = models.IntegerField(db_column='intPhase')  # Field name made lowercase.
    vchmode = models.CharField(db_column='vchMode', max_length=45, blank=True, null=True)  # Field name made lowercase.
    intmaxpower = models.IntegerField(db_column='intMaxPower', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'socket_type'


class UpdateLog(models.Model):
    intlogid = models.AutoField(db_column='intLogID', primary_key=True)  # Field name made lowercase.
    vchgroupid = models.CharField(db_column='vchGroupID', max_length=8)  # Field name made lowercase.
    vchtype = models.CharField(db_column='vchType', max_length=50)  # Field name made lowercase.
    vchdescription = models.CharField(db_column='vchDescription', max_length=100)  # Field name made lowercase.
    dttupdatedate = models.CharField(db_column='dttUpdateDate', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'update_log'


class ValueAddCard(models.Model):
    vchcardid = models.CharField(db_column='vchCardID', primary_key=True, max_length=25)  # Field name made lowercase.
    intuserpaymentrecordid = models.IntegerField(db_column='intUserPaymentRecordID', blank=True, null=True)  # Field name made lowercase.
    intcompanypaymentrecordid = models.IntegerField(db_column='intCompanyPaymentRecordID', blank=True, null=True)  # Field name made lowercase.
    dblcardvalue = models.FloatField(db_column='dblCardValue')  # Field name made lowercase.
    datdateissue = models.DateField(db_column='datDateIssue')  # Field name made lowercase.
    blnused = models.IntegerField(db_column='blnUsed')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'value_add_card'
