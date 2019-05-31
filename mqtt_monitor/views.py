# -*- coding: utf-8 -*-
from django.shortcuts import render
from datetime import datetime, timedelta, timezone
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.reverse import reverse
from bmw.models import ChargerInfo, ChargerState, ChargerModel, ChargingRecord, ChargerInfo, BasicSetting, ChargerGroup, ChargerStateLog, ChargerNetworkLog
from threading import Thread
import paho.mqtt.client as mqtt
import json

#MQTTHOST = "127.0.0.1"
MQTTHOST = "mqtt.e-chong.com"
MQTTPORT = 1883
mqttClient = mqtt.Client()

def isEmpty(s):
    return bool(not s or not s.strip())


class ChargerPoint(object):
    def __init__(self, chargerId, jsonList):
        self.chargerId = chargerId
        self.jsonList = jsonList

    def NetworkLogMsg(self):
        dic = {
            "vchchargerid": self.chargerId,
            #"lastMessageTime": datetime(),
            "lastcommandstatus": self.jsonList[2]
        }
        ChargerNetworkLog.objects.create(**dic)

    def AuthorizeMsg(self):
        """
        dic = {
            "vchchargerid":self.chargerId,
            "intchargingcode":0
        }
        ChargingRecord.objects.create(**dic)
        """
        pass

    def BootnotificationMsg(self):
        content = self.jsonList[3]
        #有该cid判断数据是否有改变再更新
        try:
            charger_info = ChargerInfo.objects.get(vchchargerid=self.chargerId)
            if charger_info.vchvenderid != content["chargePointVendor"]:
                charger_info.vchvenderid = content["chargePointVendor"]
            if charger_info.vchmodelid != content["chargePointModel"]:
                charger_info.vchmodelid = content["chargePointModel"]
            #if charger_info.vchserialno != content["chargeBoxSerialNumber"]:
            #    charger_info.vchserialno = content["chargeBoxSerialNumber"]
            if charger_info.vchfirmwarever != content["firmwareVersion"]:
                charger_info.vchfirmwarever = content["firmwareVersion"]   
            if charger_info.vchprotocol != content["protocolVersion"]:
                charger_info.vchprotocol = content["protocolVersion"]
            #if charger_info.vchip != content["chargerIp"]:
            #    charger_info.vchip = content["chargerIp"]
            if charger_info.vchmac != content["mac"]:
                charger_info.vchmac = content["mac"]
            charger_info.save()
            
        except KeyError:
            print("BootnotificationMsg key err!")
            
        except ObjectDoesNotExist:
            print('BootnotificationMsg-> ObjectDoesNotExist')
            dic = {
                "vchchargerid": self.chargerId,
                "vchvenderid": content["chargePointVendor"],
                #"vchgrouptransformer": 0,
                "vchmodelid": content["chargePointModel"],
                #"vchgroupid": 0,
                #"vchserialno": content["chargeBoxSerialNumber"],   #没有该字段
                "vchfirmwarever": content["firmwareVersion"],
                #"datmanufacturingdate": content["chargerTime"],    #需要时间格式对应datefield
                #"dblaccumlatedpower": 0,
                #"dblaccumlatedminute": 0,
                "vchprotocol": content["protocolVersion"],
                #"vchip": content["chargerIp"],     #没有该字段
                "vchmac": content["mac"]
            }
            ChargerInfo.objects.create(**dic)

    def HeartBeatMsg(self):
        content = self.jsonList[3]
        try:
            charger_state = ChargerState.objects.get(vchchargerid=self.chargerId)
            if charger_state.vchstate != content["status"]:
                charger_state.vchstate = content["status"]
            charger_state.dttlastconntime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            charger_state.save()

        except ObjectDoesNotExist:
            print('HeartBeatMsg-> charger_state cid[%s] not exist' % self.chargerId)
            #ChargerState.objects.create(vchchargerid=self.chargerId, vchState=content["status"])

    def MetervalueMsg(self):
        content = self.jsonList[3]["meterValue"]
        try:
            dic = {
                "dttlastconntime": content["timestamp"],
                "intconsumedenergy": content["ConsumedEnergy"],      #???
                #"intcharingvoltage": content["SupplyVoltage"],          #字段不存在
                "intchargingcurrent": content["SupplyCurrent"],
                #"intchargingphase": content["SupplyPhase"],         #字段不存在
                "intelapsedtime": content["ElapsedTime"]
            }

            ChargerState.objects.filter(vchchargerid=self.chargerId).update(**dic)
        except KeyError:
            print("MetervalueMsg key err!")
        except Exception:
            print("MetervalueMsg update error! cid[%s]" % self.chargerId)

    def StartTransactionMsg(self):
        content = self.jsonList[3]
        """
        [2, "05010210-20190301T170031-3816466758", "StartTransaction", {
                "chargerId":    "05010210",
                "connectorId":  3,
                "idTag":    "AE4726C00F880400C818002000000015",
                "meterstart":   864,
                "timestamp":    "2019-03-01T17:00:31",
                "chargingCycle":    14,
                "maxPhase": 1,
                "maxFeedback":  11169,
                "maxCurrent":   32,
                "ConsumedEnergy":   15,
                "SupplyVoltage":    221958,
                "SupplyCurrent":    11140,
                "duration": 2880,
                "delay":    0,
                "reason":   "Local",
                "reasonDetail": "RFID"
            }]
        """
        try:
            dic = {
                "vchchargerid": self.chargerId,
                "vchcardid": content["idTag"],
                "intchargingcode": content["chargingCycle"],
                "dttstarttime": content["timestamp"],
                "intmaxphase": content["maxPhase"],
                "intmaxsupplycurrent": content["maxFeedback"]/1000,
                "intmaxcurrent": content["maxCurrent"],
                "dblenergy": content["ConsumedEnergy"]/1000,
                #"intSupplyVol": content["SupplyVoltage"],  #字段不存在
                #?: content["SupplyCurrent"],    #字段不存在
                #"intduration": content["duration"],     #字段不存在
                #"vchreason": content["reason"],     #字段不存在
                "vchremark": content["reasonDetail"]
            }
            ChargingRecord.objects.create(**dic)
        except KeyError:
            print("StartTransactionMsg key err!")
        except Exception:
            print("StartTransactionMsg update error! cid[%s]" % self.chargerId)

    def StatusNotificationMsg(self):
        content = self.jsonList[3]
        try:
            if content["errorCode"] != "noError":
                dic = {
                    "vchchargerid": self.chargerId,
                    "errorcode": content["errorCode"],
                    "status": content["status"],
                    "dtttime": content["timestamp"],
                    "connectorfeedback": content["submode"]["connectorFeeback"],
                    "lastcycle": content["lastchargingcycle"]
                }
                ChargerStateLog.objects.create(**dic)

            ChargerState.objects.filter(vchchargerid=self.chargerId).update(vchstate=content["status"])
        except KeyError:
            raise KeyError("StatusNotificationMsg key err!")
        except Exception:
            print("StatusNotificationMsg update error! cid[%s]" % self.chargerId)

def process_data(msg):
    topic = msg.topic.split("/")           #Message/05010103/MeterValues
    if len(topic) < 3 or isEmpty(topic[1]) or isEmpty(topic[2]):
        print("topic[%s] is error!" % msg.topic)
        #return

    if isEmpty(msg.payload):
        print("Msg is null!")
        return

    chargerId = topic[1]
    msgType = topic[2]
    jsonList = json.loads(msg.payload.decode())
    print(jsonList)
    charger = ChargerPoint(chargerId, jsonList)

    charger.NetworkLogMsg()
    if msgType=="Authorize":
        charger.AuthorizeMsg()
    elif msgType=="BootNotification":
        charger.BootnotificationMsg()
    elif msgType=="Heartbeat":
        charger.HeartBeatMsg()
    elif msgType=="MeterValues":
        charger.MetervalueMsg()
    elif msgType=="StartTransaction":
        charger.StartTransactionMsg()
    elif msgType=="StatusNotification":
        charger.StatusNotificationMsg()
    else:
        print("Unkown command [%s]" % msgType)


# 连接MQTT服务器
def on_mqtt_connect():
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()     #另开线程监听
 
 
# publish 消息
def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)

# 消息处理函数
def on_message_come(lient, userdata, msg):
    #print(msg.topic + " " + ":" + str(msg.payload))
    t=Thread(target=process_data,args=(msg,))
    t.setDaemon(True)
    t.start()   #子线程去处理数据,若性能不够可以使用celery
    t.join(2)

# subscribe 消息
def on_subscribe():
    mqttClient.subscribe("Message/#", 2)
    #mqttClient.subscribe([("1/topic", 0), ("2/topic", 2)])
    mqttClient.on_message = on_message_come
 
 
def __main():
    on_mqtt_connect()
    on_subscribe()
 
__main()

