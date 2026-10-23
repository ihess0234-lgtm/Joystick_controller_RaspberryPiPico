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
    MESSAGE = re.sub(r' {1}', '=', MESSAGE)

    MESSAGE_SPLIT = re.split(r'={1,2}', MESSAGE)

    xAxis = int(MESSAGE_SPLIT[0])
    yAxis = int(MESSAGE_SPLIT[1])

    #Still
    if xAxis > 47000 and xAxis < 49000 and yAxis > 49000 and yAxis < 51000:
        print("Still")

    #Moving forward right
    elif xAxis == 65535 and yAxis == 65535:
        print(">^")
    
    #Moving forward left 
    elif xAxis == 65535 and yAxis >= 304 and yAxis < 65535:
        print("<^")

    #Moving backward right
    elif xAxis >= 304 and xAxis < 65535 and yAxis == 65535:
        print(">v")
        
    #Moving backward left
    elif xAxis >= 304 and xAxis < 65535 and yAxis >= 304 and yAxis < 65535:
        print("<v")





mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("mqtt-dashboard.com")
mqttc.loop_forever()
