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

    def ChangeChargerState(self,dic):
        try:
            charger_state = ChargerState.objects.get(vchchargerid=self.chargerId)
            if charger_state.vchcommand != dic["vchcommand"]:
                charger_state.vchcommand = dic["vchcommand"]
            if charger_state.vchstate != dic["vchstate"]:
                charger_state.vchstate = dic["vchstate"]
            if "intconsumedenergy" in dic and charger_state.intconsumedenergy != dic["intconsumedenergy"]:
                charger_state.intconsumedenergy != dic["intconsumedenergy"]
            if "intchargingcurrent" in dic and charger_state.intchargingcurrent != dic["intchargingcurrent"]:
                charger_state.intchargingcurrent != dic["intchargingcurrent"]
            if "intelapsedtime" in dic and charger_state.intelapsedtime != dic["intelapsedtime"]:
                charger_state.intelapsedtime != dic["intelapsedtime"]
            if "dttlastconntime" in dic and charger_state.dttlastconntime != dic["dttlastconntime"]:
                charger_state.dttlastconntime != dic["dttlastconntime"]
            else:
                charger_state.dttlastconntime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            charger_state.save()

        except ObjectDoesNotExist:
            print('ChangeChargerState cid[%s] vchcommand[%s]-> ObjectDoesNotExist' % (self.chargerId, dic["vchcommand"]))
            dic_s = {
                "vchchargerid": self.chargerId,
                "dttlastconntime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "vchcommand": dic["vchcommand"],
                "vchstate": dic["vchstate"]
            }
            ChargerState.objects.create(**dic_s)

    def NetworkLogMsg(self):
        try:
            charger_network_log = ChargerNetworkLog.objects.get(vchchargerid=self.chargerId)
            if charger_network_log.lastcommandstatus != self.jsonList[2]:
                charger_network_log.lastcommandstatus = self.jsonList[2]
            charger_network_log.lastmessagetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            charger_network_log.save()
        except ObjectDoesNotExist:
            print('NetworkLogMsg-> ObjectDoesNotExist cid[%s]' % self.chargerId)
            dic = {
                "vchchargerid": self.chargerId,
                "lastmessagetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
            if charger_info.vchvendorid != content["chargePointVendor"]:
                charger_info.vchvendorid = content["chargePointVendor"]
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
                "vchvendorid": content["chargePointVendor"],
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

        dic_s = {
            "vchcommand": "Bootnotification",
            "vchstate": "Bootnotification"
        }
        self.ChangeChargerState(dic_s)

    def HeartBeatMsg(self):
        content = self.jsonList[3]
        dic_s = {
            "vchcommand": "HeartBeat",
            "vchstate": "Available"
            #"vchstate": content["status"]
        }
        self.ChangeChargerState(dic_s)

    def MetervalueMsg(self):
        content = self.jsonList[3]["meterValue"]
        try:
            dic_s = {
                "dttlastconntime": content["timestamp"],
                "intconsumedenergy": content["ConsumedEnergy"],      #???
                #"intcharingvoltage": content["SupplyVoltage"],          #字段不存在
                "intchargingcurrent": content["SupplyCurrent"],
                #"intchargingphase": content["SupplyPhase"],         #字段不存在
                "intelapsedtime": content["ElapsedTime"],
                "vchcommand": "MeterValues",
                "vchstate": "charging"
            }

            self.ChangeChargerState(dic_s)
        except KeyError:
            print("MetervalueMsg key err!")

    def StartTransactionMsg(self):
        content = self.jsonList[3]
        """
[{'idTag': 'DEDA27C0E3880400C818002000000015', 'maxPhase': 1, 'maxFeedback': 30390, 'chargingCycle': 105, 'delay': 0, 'duration': 2880, 'connectorId': 3,
  'reason': 'Local', 'reasonDetail': 'RFID', 'timestamp': '2019-06-06T16:07:15', 'chargerId': '05010202', 'meterstart': 395276}]
        """
        try:
            dic = {
                "vchchargerid": self.chargerId,
                "vchcardid": content["idTag"],
                "intchargingcode": content["chargingCycle"],
                "dttstarttime": content["timestamp"],
                "intmaxphase": content["maxPhase"],
                "intmaxsupplycurrent": content["maxFeedback"]/1000,
                #"intmaxcurrent": content["maxCurrent"],          #字段不存在
                #"dblenergy": content["ConsumedEnergy"]/1000,     #字段不存在
                #"intSupplyVol": content["SupplyVoltage"],  #字段不存在
                #?: content["SupplyCurrent"],    #字段不存在
                "intduration": content["duration"],
                "vchreason": content["reason"],
                "vchremark": content["reasonDetail"],
                "dblenergy": 0,
                "intmaxcurrent": 0,
                "intmincurrent": 0
            }
            ChargingRecord.objects.create(**dic)

            dic_s = {
                "vchcommand": "StartTransaction",
                "vchstate": "StartTransaction"
            }
            self.ChangeChargerState(dic_s)
        except KeyError:
            print("StartTransactionMsg key err! [%s]" % content)
        #except Exception:
        #    print("StartTransactionMsg update error! cid[%s][%s]" % (self.chargerId, content))

    def StopTransactionMsg(self):
#[StopTransaction][[2, '05010207-20190617T112749-2167368079', 'StopTransaction', {'reasonDetail': 'RFID', 'timestamp': '2019-06-17T11:27:49',
#'chargingCycle': 134, 'transactionID': 684056, 'reason': 'Local', 'chargerId': '05010207', 'meterStop': 1670052, 'idTag': 'AE3922C075880400C818002000000015'}]]
        content = self.jsonList[3]
        try:
            dic = {
                "vchchargerid": self.chargerId,
                "vchcardid": content["idTag"],
                "intchargingcode": content["chargingCycle"],        #intchargingcode 判断是否存在，不存在就插入一条
                "dttstarttime": content["timestamp"],
                "vchreason": content["reason"],
                "vchremark": content["reasonDetail"],
                "vchsocketid": '0',
                "vchrecordstate": '0',
                "vchopenrecord": '0',
                "vchcloserecord": '0',
                "intduration": 0,
                "dblenergy": 0,
                "intmaxsupplycurrent": 0,
                "intmaxcurrent": 0,
                "intmincurrent": 0,
                "intsafecurrent": 0,
                "intpwnchangedelay": 0
            }
            ChargingRecord.objects.create(**dic)

            dic_s = {
                "vchcommand": "StopTransaction",
                "vchstate": "StopTransaction"
            }
            self.ChangeChargerState(dic_s)
        except KeyError:
            print("StopTransactionMsg key err! [%s]" % content)
        except Exception:
            print("StopTransactionMsg update error! cid[%s][%s]" % (self.chargerId, content))

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

            dic_s = {
                "vchcommand": "StatusNotification",
                "vchstate": content["status"]
            }
            self.ChangeChargerState(dic_s)
        except KeyError:
            raise KeyError("StatusNotificationMsg key err!")
        except Exception:
            print("StatusNotificationMsg update error! cid[%s][%s]" % (self.chargerId, content))

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
    #print(jsonList)
    charger = ChargerPoint(chargerId, jsonList)

    charger.NetworkLogMsg()
    if msgType=="Authorize":
        charger.AuthorizeMsg()
    elif msgType=="BootNotification":
        charger.BootnotificationMsg()
    elif msgType=="HeartBeat":
        charger.HeartBeatMsg()
    elif msgType=="MeterValues":
        charger.MetervalueMsg()
    elif msgType=="StartTransaction":
        charger.StartTransactionMsg()
    elif msgType=="StopTransaction":
        charger.StopTransactionMsg()
    elif msgType=="StatusNotification":
        charger.StatusNotificationMsg()
    else:
        print("Unkown command [%s][%s]" % (msgType,jsonList))

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
