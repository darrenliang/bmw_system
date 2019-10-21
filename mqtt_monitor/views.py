# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db import connection
from django.db.models import Q
from datetime import datetime, timedelta, timezone
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework import generics, permissions, status, authentication
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from bmw.models import ChargerInfo, ChargerState, ChargerModel, ChargingRecord, ChargerInfo, BasicSetting, ChargerGroup, ChargerStateLog, ChargerNetworkLog
import threading
from threading import Thread
import paho.mqtt.client as mqtt
import json,time
from mqtt_monitor.models import ChargersMeterValue

#MQTTHOST = "127.0.0.1"
MQTTHOST = "mqtt.e-chong.com"
MQTTPORT = 1883
monitor_dic = {}
last_request_time = 0
mutex = threading.Lock()

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

        gid = self.chargerId[0:6]
        if(gid in monitor_dic.keys()):
            #try:
                mutex.acquire()
                if self.chargerId not in monitor_dic[gid]["cid_dic"].keys() or monitor_dic[gid]["cid_dic"][self.chargerId]["state"] == "disconnect":     #新来的或重新连接的cid设为connecting状态
                    monitor_dic[gid]["cid_dic"][self.chargerId] = {}
                    monitor_dic[gid]["cid_dic"][self.chargerId]["state"] = "connecting"
                else:
                    monitor_dic[gid]["cid_dic"][self.chargerId]["state"] = "connected"

                monitor_dic[gid]["cid_dic"][self.chargerId]["timestamp"] = int(time.time())
                mutex.release()

                dic_s = {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "vchstate": monitor_dic[gid]["cid_dic"][self.chargerId]["state"],
                    "vchgroupid": gid,
                    "vchchargerid": self.chargerId,
                    "intconsumedenergy": content["ConsumedEnergy"],
                    "intchargingcurrent": content["SupplyCurrent"],
                    "intelapsedtime": content["ElapsedTime"]
                }
                ChargersMeterValue.objects.create(**dic_s)  #所有数据暂时插入一个表中，若每个gid分配一个表需要涉及到动态建表删表等问题
            #except Exception:
                #print("MetervalueMsg insert ChargersMeterValue error!")

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
                "intmincurrent": 0,
                "intsafecurrent": 0,
                "intpwnchangedelay": 0
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

    connection.close()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# 消息处理函数
def on_message_come(client, userdata, msg):
    #print(msg.topic + " " + ":" + str(msg.payload))
    t=Thread(target=process_data,args=(msg,))
    t.setDaemon(True)
    t.start()   #子线程去处理数据,若性能不够可以使用celery
    t.join(2)

# disconnect
def on_disconnect(client, userdata, rc):
    print("on_disconnect: error code[%d]" % rc)
    try:
        mqtt_client()
    except Exception:
        pass

def mqtt_client():
    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_message = on_message_come
    mqttClient.on_disconnect = on_disconnect
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.subscribe("Message/#", 2)            #mqttClient.subscribe([("1/topic", 0), ("2/topic", 2)])
    mqttClient.loop_start()

# 监听monitor_dic,定期清除超时的gid
def clear_gid_timer():
    global last_request_time,monitor_dic
    while True:
        time.sleep(10)
        now = int(time.time())
        for key,value in list(monitor_dic.items()):
            if now - value["request_time"] > 60:     #30分没有该gid请求就不再监听该gid数据
                print("del gid[%s]------------------------now=%d-----request_time=%d" % (key, now, value["request_time"]))
                mutex.acquire()
                del monitor_dic[key]
                mutex.release()
                ChargersMeterValue.objects.filter(vchgroupid=key).delete()

        if now - last_request_time > 60:
            print('del------------dbtable',now, last_request_time)
            ChargersMeterValue.objects.all().delete()       #30分无任何请求就清空ChargersMeterValue表

#定时更新数据库cid状态值;
def cid_state_timer():
    global monitor_dic
    num = 0
    while True:
        num = num + 1
        time.sleep(1)
        now = int(time.time())
        for gid,value in list(monitor_dic.items()):
            for cid,value in list(monitor_dic[gid]["cid_dic"].items()):
                if now - monitor_dic[gid]["cid_dic"][cid]["timestamp"] > 1:
                    if monitor_dic[gid]["cid_dic"][cid]["state"] != "disconnect":
                        mutex.acquire()
                        monitor_dic[gid]["cid_dic"][cid]["state"] = "disconnect"
                        mutex.release()
                        dic_s = {
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "vchstate": "disconnect",
                            "vchgroupid": gid,
                            "vchchargerid": cid,
                            "intconsumedenergy": -1,
                            "intchargingcurrent": -1,
                            "intelapsedtime": -1
                        }
                        ChargersMeterValue.objects.create(**dic_s)

def __main():
    mqtt_client()

    #device.html页面相关处理逻辑
    t1 = Thread(target=cid_state_timer)
    t2 = Thread(target=clear_gid_timer)
    t1.start()
    t2.start()

__main()

#监听webuser请求
class GetChargersRealTimeDataView(APIView):
    """
    This view return line charts datas for device.html
    """
    def get(self, request):
        global last_request_time, monitor_dic
        data = {}

        gid = request.GET.get("gid")
        if not gid:
            return Response("gid is none", status=status.HTTP_200_OK)
        time_step = int(request.GET.get("time_step"))    #1->5min;2->15min;3->1hour;4->4hours;5->1day
        time_step = time_step if time_step else 1
        end_time = datetime.now()

        """
        request_time:       某gid最近一次请求时间
        first_request_time: 某gid首次请求时间
        last_request_time:  所有gid最近一次的请求时间
        """
        if(gid in monitor_dic.keys()):      #已创建就直接读数据库
            queryset_gid = ChargersMeterValue.objects.filter(vchgroupid=gid)
            for cid,value in list(monitor_dic[gid]["cid_dic"].items()):
                start_time = self.get_start_time(time_step, end_time)
                #start_time = start_time if start_time > monitor_dic[gid]["first_request_time"] else monitor_dic[gid]["first_request_time"]
                orig_data = self.get_orig_data_fromdb(cid, start_time, end_time, queryset_gid)
                if orig_data:
                    data[cid] = self.process_data(orig_data,time_step, start_time)

            mutex.acquire()
            try:
                monitor_dic[gid]["request_time"] = last_request_time = int(time.time())
            except Exception:
                pass
            mutex.release()

        else:                       #添加gid相关信息到monitor_dic
            mutex.acquire()
            try:
                monitor_dic[gid] = {}
                monitor_dic[gid]["cid_dic"] = {}
                monitor_dic[gid]["first_request_time"] = datetime.now()
                monitor_dic[gid]["request_time"] = last_request_time = int(time.time())
            except Exception:
                pass
            mutex.release()
        #print(data)
        return Response(data, status=status.HTTP_200_OK)

    def get_start_time(self, time_step, end_time):
        """
        获取起始时间点
        """
        if time_step == 1:
            return end_time - timedelta(minutes=5)
        elif time_step == 2:
            return end_time - timedelta(minutes=15)
        elif time_step == 3:
            return end_time - timedelta(hours=1)
        elif time_step == 4:
            return end_time - timedelta(hours=4)
        elif time_step == 5:
            return end_time - timedelta(days=1)
        else:
            return end_time - timedelta(minutes=5)

    def datetime_to_timestamp(self, dt):
        return int(time.mktime(dt.timetuple()))

    def process_data(self, orig_data, time_step, start_time):
        """
        将原始1秒一次的数据量压缩，减轻前端显示压力(5min的数据量较小不需要压缩)
        对于15min以上的数据，由于'/'数据处理较为复杂，暂时使用简单的算法：
        time_step时间段内空值数量大于非空值，该时间段取值为空，否则该时间段取值为非空值的平均值
        """
        supply_current_list = []    #电桩实时电流信息
        consumed_energy_list = []   #电桩实时电量信息
        elapsed_time = 0      #充电时间
        timestamp_list = []         #web页面x轴时间列表
        second_1 = timedelta(seconds=1)
        step_list = [-1,-1,45,180,720,4320]     #前两个值占位，45表示15min分成20段每段长度45秒...

        if time_step == 1:          #5min不压缩
            for item in orig_data:
                start_time = start_time+second_1
                if item == '/':
                    supply_current_list.append('/')
                    consumed_energy_list.append('/')
                else:
                    supply_current_list.append(item.intchargingcurrent if item.intchargingcurrent != -1 else '/')
                    consumed_energy_list.append(item.intconsumedenergy if item.intconsumedenergy != -1 else '/')
                    elapsed_time = (item.intelapsedtime if item.intelapsedtime != -1 else elapsed_time)
                timestamp_list.append(start_time.strftime('%H:%M:%S'))

        else:
            for i in range(20):     #压缩为20个时间节点
                start_time = start_time+second_1*step_list[time_step]
                nul_num = sum_sc = sum_ce = 0
                for item in orig_data[i*step_list[time_step]:(i+1)*step_list[time_step]]:
                    if item != '/' and item.vchstate != "disconnect":
                        sum_sc = sum_sc + int(item.intchargingcurrent)
                        sum_ce = sum_ce + int(item.intconsumedenergy)
                        elapsed_time = item.intelapsedtime
                    else:
                        nul_num = nul_num + 1

                if nul_num > int(step_list[time_step]/4*3):      #空值占3/4，取空值
                    supply_current_list.append('/')
                    consumed_energy_list.append('/')
                else:                          #有效值占多数，取平均值
                    supply_current_list.append(int(sum_sc/(step_list[time_step]-nul_num)))
                    consumed_energy_list.append(int(sum_ce/(step_list[time_step]-nul_num)))

                timestamp_list.append(start_time.strftime('%H:%M:%S'))

        dic = {
                "supply_current_list": supply_current_list,
                "consumed_energy_list": consumed_energy_list,
                "elapsed_time": elapsed_time,
                "timestamp_list": timestamp_list
              }
        return dic
    def get_orig_data_fromdb(self, cid, start_time, end_time, queryset_gid):
        """
        一段时间内某个cid的mqtt数据流可能的情况：
        1.|++++++++++++++++|    #数据正常无掉线
        2.|++++        ++++|    #有数据->无数据->有数据
          |++++  ++++  ++++|    #2的派生类型
        3.|++++            |    #前一段时间有数据，后一段时间无
          |++++  ++++      |    #3的派生类型
        4.|            ++++|    #前一段时间无数据，后一段时间有
          |      ++++  ++++|    #4的派生类型
        5.|      ++++      |    #无数据->有数据->无数据
          |   +++    +++   |    #5的派生类型
        6.|                |    #掉线无数据
        """
        #按照始末时间mqtt是否连接分为四类:1,2属于始末时间都连接;  5,6属于始末时间都掉线(或未充电); 3属于起始连接，结束未连接;  4属于起始未连接，结束时已连接
        total_list = []
        queryset_cid = queryset_gid.filter(vchchargerid=cid).order_by("id")
        second_1 = timedelta(seconds=1)
        len_time=(end_time-start_time)/second_1
        start_con = True if queryset_cid.filter(time__range=(start_time-second_1, start_time+second_1), vchstate="connected") else False   #起始时间是否连接
        end_con = True if queryset_cid.filter(time__range=(end_time-second_1*2, end_time), vchstate="connected") else False         #结束时间是否连接
        #start_time+second_1目的是避免和start_con的范围冲突；end_time+second_1*2目的是适配掉线后的超时判断时间
        con_discon_list = queryset_cid.filter(time__range=(start_time+second_1, end_time+second_1*2),   #例：|++++(disconnect)   (connecting)++++(disconnect)   (connecting)++++|
                                              vchstate__in=["connecting","disconnect"]).values()[:]
        #for item in queryset_cid.filter(time__range=(start_time+second_1, end_time+second_1*3)):
        #    print(item.vchstate)
        if start_con and end_con:           #起始末尾都连接:对应第1,2两种情况
            print("22222->|++++  ++++  ++++|------%d---%s" % (len(con_discon_list), "OK" if len(con_discon_list)%2==0 else "ERROR"))
            has_discon = False
            for item in con_discon_list:
                if item["vchstate"] == "disconnect":
                    has_discon = True
            if has_discon:                 #第2中情况或其子类
                next_state = "disconnect"
                time1 = start_time
                time2 = None
                for i in range(len(con_discon_list)):
                    if con_discon_list[i]["vchstate"] == next_state:
                        time2 = con_discon_list[i]["time"]
                        if next_state == "disconnect":
                            total_list += queryset_cid.filter(time__range=(time1, time2))
                        else:
                            total_list += (self.datetime_to_timestamp(time2) - self.datetime_to_timestamp(time1)) * ['/']
                        next_state = "connecting" if next_state == "disconnect" else "disconnect"
                        time1 = time2
                total_list += queryset_cid.filter(time__range=(time1, end_time))
            else:                           #第1种情况
                total_list = queryset_cid.filter(time__range=(start_time, end_time))

        elif not start_con and not end_con: #起始末尾都掉线:对应第5,6两种情况
            print("55555->|   +++    +++   |------%d---%s" % (len(con_discon_list), "OK" if len(con_discon_list)%2==0 else "ERROR"))
            has_con = False
            for item in con_discon_list:
                if item["vchstate"] == "connecting":
                    has_con = True
            if has_con:                #第5种情况或其子类
                next_state = "connecting"
                time1 = start_time
                time2 = None
                for i in range(len(con_discon_list)):
                    if con_discon_list[i]["vchstate"] == next_state:
                        time2 = con_discon_list[i]["time"]
                        if next_state == "connecting":
                            total_list += (self.datetime_to_timestamp(time2) - self.datetime_to_timestamp(time1)) * ['/']
                        else:
                            total_list += queryset_cid.filter(time__range=(time1, time2))
                        next_state = "connecting" if next_state == "disconnect" else "disconnect"
                        time1 = time2
                total_list += (self.datetime_to_timestamp(end_time) - self.datetime_to_timestamp(time1)) * ['/']
            else:                           #第6种情况
                total_list += (self.datetime_to_timestamp(end_time) - self.datetime_to_timestamp(start_time)) * ['/']
        elif start_con and not end_con:     #起始连接末尾掉线:对应第3种情况及其子类
            print("33333->|++++  ++++      |------%d---%s" % (len(con_discon_list), "OK" if len(con_discon_list)%2==1 else "ERROR"))
            if len(con_discon_list) > 0:
                next_state = "disconnect"
                time1 = start_time
                time2 = None
                for i in range(len(con_discon_list)+1):     #+1表示添加一个连接数据，模拟连接，转化为第2种情况的处理方法
                    if i == len(con_discon_list):           #结尾数据段需要填充'/'
                        total_list += (self.datetime_to_timestamp(end_time) - self.datetime_to_timestamp(con_discon_list[i-1]["time"])) * ['/']
                        break
                    if con_discon_list[i]["vchstate"] == next_state:
                        time2 = con_discon_list[i]["time"]
                        if next_state == "disconnect":
                            total_list += queryset_cid.filter(time__range=(time1, time2))
                        else:
                            total_list += (self.datetime_to_timestamp(time2) - self.datetime_to_timestamp(time1)) * ['/']
                        next_state = "connecting" if next_state == "disconnect" else "disconnect"
                        time1 = time2

        else:                               #起始掉线末尾连接:对应第4种情况及其子类
            print("44444->|      ++++  ++++|------%d---%s" % (len(con_discon_list), "OK" if len(con_discon_list)%2==1 else "ERROR"))
            if len(con_discon_list) > 0:
                next_state = "connecting"
                time1 = start_time
                time2 = None
                for i in range(len(con_discon_list)+1):     #+1表示添加一个掉线数据，模拟掉线，转化为第5种情况的处理方法
                    if i == len(con_discon_list):
                        total_list += queryset_cid.filter(time__range=(con_discon_list[i-1]["time"], end_time))
                        break
                    if con_discon_list[i]["vchstate"] == next_state:
                        time2 = con_discon_list[i]["time"]
                        if next_state == "connecting":
                            total_list += (self.datetime_to_timestamp(time2) - self.datetime_to_timestamp(time1)) * ['/']
                        else:
                            total_list += queryset_cid.filter(time__range=(time1, time2))
                        next_state = "connecting" if next_state == "disconnect" else "disconnect"
                        time1 = time2

        return total_list

    """
    def get_orig_data_fromdb_bak(self, cid, start_time, end_time, queryset_gid):

        一段时间内某个cid的mqtt数据流可能的情况：
        1.|++++++++++++++++|    #数据正常无掉线
        2.|++++        ++++|    #有数据->无数据->有数据
          |++++  ++++  ++++|    #2的派生类型
        3.|++++            |    #前一段时间有数据，后一段时间无
          |++++  ++++      |    #3的派生类型
        4.|            ++++|    #前一段时间无数据，后一段时间有
          |      ++++  ++++|    #4的派生类型
        5.|      ++++      |    #无数据->有数据->无数据
          |   +++    +++   |    #5的派生类型
        6.|                |    #掉线无数据

        #按照始末时间mqtt是否连接分为四类:1,2属于始末时间都连接;  5,6属于始末时间都掉线(或未充电); 3属于起始连接，结束未连接;  4属于起始未连接，结束时已连接
        total_list = []
        queryset_cid = queryset_gid.filter(vchchargerid=cid).order_by("id")
        second_1 = timedelta(seconds=1)
        len_time=(end_time-start_time)/second_1
        start_con = True if queryset_cid.filter(time__range=(start_time-second_1, start_time+second_1), vchstate="connected") else False   #起始时间是否连接
        end_con = True if queryset_cid.filter(time__range=(end_time-second_1*2, end_time), vchstate="connected") else False         #结束时间是否连接
        #start_time+second_1目的是避免和start_con的范围冲突；end_time+second_1*2目的是适配掉线后的超时判断时间
        discon_list = queryset_cid.filter(time__range=(start_time+second_1, end_time+second_1*2), vchstate="disconnect")      #例：|++++(disconnect)   (new_connect)++++(disconnect)   (new_connect)++++|
        new_con_list = queryset_cid.filter(time__range=(start_time+second_1, end_time), vchstate="new_connect")
        #for item in queryset_cid.filter(time__range=(start_time+second_1, end_time+second_1*3)):
        #    print(item.vchstate)

        if start_con and end_con:           #起始末尾都连接:对应第1,2两种情况
            print("22222->|++++  ++++  ++++|", len(discon_list), len(new_con_list))
            if discon_list:                 #第2中情况或其子类
                #判断len(discon_list)是否等于len(new_con_list)
                total_list += queryset_cid.filter(time__range=(start_time, discon_list[0].time))
                for i in range(len(discon_list)):
                    total_list += (self.datetime_to_timestamp(new_con_list[i].time) - self.datetime_to_timestamp(discon_list[i].time)) * ['/']      #掉线期间的数据填充为'/'
                    try:                    #discon_list[i+1]如果异常说明到结尾
                        if discon_list[i+1]:
                            total_list += queryset_cid.filter(time__range=(new_con_list[i].time, discon_list[i+1].time))
                    except Exception:
                        total_list += queryset_cid.filter(time__range=(new_con_list[i].time, end_time))
            else:                           #第1种情况
                total_list = queryset_cid.filter(time__range=(start_time, end_time))

        elif not start_con and not end_con: #起始末尾都掉线:对应第5,6两种情况
            print("55555->|   +++    +++   |", len(discon_list), len(new_con_list))
            if new_con_list:                #第5种情况或其子类
                total_list += (self.datetime_to_timestamp(new_con_list[0].time) - self.datetime_to_timestamp(start_time)) * ['/']      #掉线期间的数据填充为'/'
                if len(new_con_list) <= len(discon_list):
                    for i in range(len(new_con_list)):
                        total_list += queryset_cid.filter(time__range=(new_con_list[i].time, discon_list[i].time))
                        try:                    #new_con_list[i+1]如果异常说明到结尾
                            if new_con_list[i+1]:
                                total_list += (self.datetime_to_timestamp(new_con_list[i+1].time) - self.datetime_to_timestamp(discon_list[i].time)) * ['/']
                        except Exception:
                            total_list += (self.datetime_to_timestamp(end_time) - self.datetime_to_timestamp(discon_list[i].time)) * ['/']
            else:                           #第6种情况
                total_list += (self.datetime_to_timestamp(end_time) - self.datetime_to_timestamp(start_time)) * ['/']

        elif start_con and not end_con:     #起始连接末尾掉线:对应第3种情况及其子类
            print("33333->|++++  ++++      |", len(discon_list), len(new_con_list))
            for i in range(len(discon_list)):
                if i == 0:
                    total_list += queryset_cid.filter(time__range=(start_time, discon_list[i].time))
                else:
                    total_list += queryset_cid.filter(time__range=(new_con_list[i-1].time, discon_list[i].time))

                try:                        #new_con_list[i]如果异常说明到结尾
                    if new_con_list[i]:
                        total_list += (self.datetime_to_timestamp(new_con_list[i].time) - self.datetime_to_timestamp(discon_list[i].time)) * ['/']
                except Exception:
                    total_list += (self.datetime_to_timestamp(end_time) - self.datetime_to_timestamp(discon_list[i].time)) * ['/']

        else:                               #起始掉线末尾连接:对应第4种情况及其子类
            print("44444->|      ++++  ++++|", len(discon_list), len(new_con_list))
            for i in range(len(new_con_list)):
                if i == 0:
                    total_list += (self.datetime_to_timestamp(new_con_list[i].time) - self.datetime_to_timestamp(start_time)) * ['/']
                else:
                    total_list += (self.datetime_to_timestamp(new_con_list[i].time) - self.datetime_to_timestamp(discon_list[i-1].time)) * ['/']    #----------------------
                try:                        #discon_list[i]如果异常说明到结尾
                    if discon_list[i]:
                        total_list += queryset_cid.filter(time__range=(new_con_list[i].time, discon_list[i].time))
                except Exception:
                    total_list += queryset_cid.filter(time__range=(new_con_list[i].time, end_time))

        return total_list
    """