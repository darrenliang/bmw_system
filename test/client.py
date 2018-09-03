import paho.mqtt.client as mqtt #import the client1


broker_address = "114.119.9.130"
# broker_address="iot.eclipse.org"
print("creating new instance")
client = mqtt.Client("P1")  # create new instance
print("connecting to broker")
client.connect(broker_address)  # connect to broker
print("Subscribing to topic", "house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic", "house/bulbs/bulb1")
client.publish("house/bulbs/bulb1", "OFF")

client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
client.connect("114.119.9.130", port=8083, keepalive=60, bind_address="")
