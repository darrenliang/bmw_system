import paho.mqtt.client as mqtt
import time
from threading import Thread
str1="""
[2, "05010210-20190301T170003-779737637", "StatusNotification", {"chargerId":    "05010210",\
"connectorId":  3,\
"errorCode":    "noError",\
"status":   "Charging3333",\
"timestamp":    "2019-03-01T17:00:03",\
"submode":  {\
"connectorFeeback": "EvReady",\
"SupportCurrent":   32,\

"parkSensor":   "NotImplemented",\
"groundLock":   "NotImplemented",\
            "cablelock":    "NoResponse"\
        },\
        "Info": 0,\
        "lastchargingcycle":    14\
    }]
"""
str2='[1,"00ed5d3f-2efa-42d5-ac88-13549b365301","Heartbeat",{"chargerID":"7500120A", "status":"1", "fwVersion":"COAB10160D/VPNCNMV19179",\
"mac":"xx:xx:xx:xx:xx", "dInput":"12345678", "dOutput":"12345678", "serial":"SZAB1234567", "fault":"147163587","model":"EV-SVG32M"}]'

str3='[2,"280dd80b-7a30-42b4-8e12-ee1e3a6f866e","BootNotification",{ "chargePointModel":"EVC32N","chargePointVendor":"EVPOWER",\
"firmwareVersion":"HK271015-2", "chargePointSerialNumber":"EG3A508010", "protocolVersion":"0.01","chargerId" :"00504004", \
"hardwareVersion":"0.001", "mac":"0008DC17CD92","chargerTime":"2016-10-28T19:18:00Z"}]'

str4='[2, "05010210-20190301T170031-3816466758", "StartTransaction", {"chargerId":"05010210","connectorId":  3,"idTag":"AE4726C00F880400C818002000000015",\
"meterstart":   864,"timestamp":"2019-03-01T17:00:31","chargingCycle":    14,"maxPhase": 1,"maxFeedback":  11169,"maxCurrent":   32,"ConsumedEnergy":   15,\
"SupplyVoltage":    221958,"SupplyCurrent":    11140,"duration": 2880,"delay":    0,"reason":   "Local","reasonDetail": "RFID"}]'

HOST = "mqtt.e-chong.com"
PORT = 1883
client = mqtt.Client()
client.connect(HOST, PORT, 60)
def test():
    t=Thread(target=publish,args=())
    t.start()
    client.loop_forever()


def publish():
    i=0
    while True:
        #time.sleep(0.001)
        print(i)
        client.publish("Message/05010102/StatusNotification",str1,2)
        client.publish("Message/05010101/Heartbeat",str2,2)
        client.publish("Message/05010218/BootNotification",str3,2)
        client.publish("Message/05010213/StartTransaction",str4,2)
        i = i + 1
        time.sleep(1)

if __name__ == '__main__':
    test()
