from django.db import models

"""
CREATE DATABASE metervaluedb;
\c metervaluedb
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE; #使用TimescaleDB扩展数据库
CREATE TABLE chargers_metervalue (
    id serial,
    time TIMESTAMPTZ NOT NULL,
    vchState varchar(20) NOT NULL,
    vchGroupID varchar(8) NOT NULL,
    vchChargerID varchar(11) NOT NULL,
    intChargingCurrent INT NOT NULL DEFAULT '0',
    intConsumedEnergy INT NOT NULL DEFAULT '0',
    intElapsedTime INT NOT NULL DEFAULT '0'
);
SELECT create_hypertable('chargers_metervalue', 'time');
"""
class ChargersMeterValue(models.Model):
    time = models.DateTimeField(db_column='time')
    vchstate = models.CharField(db_column='vchstate', max_length=20)
    vchgroupid = models.CharField(db_column='vchgroupid', max_length=8)
    vchchargerid = models.CharField(db_column='vchchargerid', max_length=11)
    intconsumedenergy = models.IntegerField(db_column='intconsumedenergy',default=0)
    intchargingcurrent = models.IntegerField(db_column='intchargingcurrent',default=0)
    intelapsedtime = models.IntegerField(db_column='intelapsedtime',default=0)

    class Meta:
        app_label = 'mqtt_monitor'
        managed = False
        db_table = 'chargers_metervalue'
        #unique_together = (('real_name', 'id_card'),)
