import paho.mqtt.client as mqtt
import re

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    
def on_message(client, userdata, msg):
    if msg.topic == "TAFE/i-hess/morse-code-respond":
        return

    MESSAGE = (str(msg.payload))

    # Remove unesasary 
    MESSAGE = re.sub(r',|"|b', '', MESSAGE)
    MESSAGE = re.sub(r"[\[\]\']", '', MESSAGE)

    # Turn spaces into = or nothing to seperate into words
    MESSAGE = re.sub(r' {2}', '=', MESSAGE)
    MESSAGE = re.sub(r' {1}', '', MESSAGE)

    # convert to MESSAGE list into LETTERS list with each item being its own letter
    LETTERS = re.split(r'={1,2}', MESSAGE)


    # Print progress converting values
    print(msg.topic+": "+str(msg.payload))
    print('Message: ', MESSAGE, "\nLetters:", LETTERS)
    print('Properly Converted:')


    # if the messages has an order that matches a string in DECIFER print off that letter. such as MESSAGE incudes = ".", "_" print("A")


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect("mqtt-dashboard.com")
mqttc.loop_forever()