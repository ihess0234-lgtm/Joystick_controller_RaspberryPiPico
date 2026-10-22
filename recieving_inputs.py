import paho.mqtt.client as mqtt
import re

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe("TAFE/i-hess/joystick-outputs")
    
def on_message(client, userdata, msg):
    if msg.topic != "TAFE/i-hess/joystick-outputs":
        return
    
    # print(msg.topic, msg.payload)

    MESSAGE = (str(msg.payload))

    # Remove unesasary 
    MESSAGE = re.sub(r',|"|b', '', MESSAGE)
    MESSAGE = re.sub(r"[\[\]\']", '', MESSAGE)

    # Turn spaces into = or nothing to seperate into words
    # MESSAGE = re.sub(r' {2}', '=', MESSAGE)
    # MESSAGE = re.sub(r' {1}', '', MESSAGE)

    print(MESSAGE)



mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("mqtt-dashboard.com")
mqttc.loop_forever()