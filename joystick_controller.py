# Thonyy Code
# from machine import Pin, ADC
# from time import sleep
# from picozero import pico_led, LED
# from umqtt.simple import MQTTClient
# import utime, time, network, dht, ujson

# VRX = ADC(Pin(27))
# VRY = ADC(Pin(26))
# SW = Pin(22, Pin.IN, Pin.PULL_UP)

# ledRed = LED(10)
# ledYellow = LED(11)
# ledGreen = LED(12)
# ledRed2 = LED(13)
# ledGreen2 = LED(8)

# MQTT_CLIENT_ID = "clientId-EoD7b24R9r"
# MQTT_BROKER    = "mqtt-dashboard.com"
# MQTT_USER      = ""
# MQTT_PASSWORD  = ""
# MQTT_TOPICS     = [b"TAFE/i-hess/joystick-inputs"]
# MQTT_TOPIC_TARGET1    = "TAFE/i-hess/joystick-inputs"


# client = None

# # wifi_ssid = "TelstraEC9E55"
# # wifi_password = "pjvgqwjrgvn6"

# wifi_ssid = "Skynet"
# wifi_password = "comewithmeifyouwanttolive"


# # Connect to wifi
# print("\nConnecting to WiFi...", end="")
# pico_led.on() # use pico_led to know when it's running
# ledRed.pulse()
# wifi = network.WLAN(network.STA_IF)
# wifi.active(True)
# wifi.connect(wifi_ssid, wifi_password)

# while not wifi.isconnected():
#   print(".", end="")
#   ledYellow.off()
#   utime.sleep(0.1)
  
# print("Connected!")
# print(f"Wi-Fi: {wifi.ifconfig()}")

# def message_callback(topic, msg):
#     if topic in MQTT_TOPICS:
#         print("Received message on topic:", topic.decode())
#         print("Message content:", msg.decode())

# def on_message(topic, msg):
#     print("Topic:", topic)
#     if topic == b'TAFE/i-hess/morse-code-respond':
#         print(f"[TARGET] Received from {topic.decode()}: {msg.decode()}")
        
#         if msg.decode() == "ledGreen2.off()":
#             ledGreen2.off()
#         if msg.decode() == "ledGreen2.on()":
#             ledGreen2.blink(.4)
            
#         if msg.decode() == "ledRed2.off()":
#             ledRed2.off()
#         if msg.decode() == "ledRed2.on()":
#             ledRed2.blink(.4)
        
#         utime.sleep(3)
#         ledRed2.off()
#         ledGreen2.off()
#     else:
#         print(f"[IGNORED] Received from {topic.decode()}")
        
# def connect_and_subscribe(client):
#     client.connect()
#     for t in MQTT_TOPICS:
#         client.subscribe(t)
#         print(f"Subscribed: {t.decode()}")
        
# def process_queue():
#     while message_queue:
#         try:
#             topic, msg, ts = message_queue.pop(0)
#             # Example processing logic
#             print(f"[{ts}] Processing message from {topic.decode()}: {msg.decode()}")
#         except Exception as e:
#             print(f"Error processing message: {e}")
            
# print("Connecting to MQTT server... ", end="")
# ledRed.pulse()
# client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
# client.set_callback(on_message)
# print("Connected!")

# connect_and_subscribe(client)
# try:
#     pico_led.on()
# finally:
#     pico_led.off()
#     ledRed2.off()
#     ledRed.off()
#     ledGreen2.off()
#     ledGreen.off()
#     ledYellow.off()
    
# while True:
#     xAxis = VRX.read_u16()
#     yAxis = VRY.read_u16()
#     switch = SW.value()
    
#     info = (xAxis, yAxis)
    
#     message = ujson.dumps(info)
#     client.publish(MQTT_TOPIC_TARGET1, message)
#     client.check_msg()
    
#     print("X-axis: " + str(xAxis) + ", Y-axis: " + str(yAxis) + ", Switch: " + str(switch))
#     if switch == 0:
#         print("Push button pressed!")
#         ledGreen.on()
#     else:
#         ledGreen.off()
#     print(" ")
#     sleep(1)

    
#     #Moving forward right
#     if xAxis == 65535 and yAxis == 65535:
#         ledRed2.off()
#         ledRed.off()
#         ledGreen2.on()
#         ledGreen.off()
#         ledYellow.off()
    
#     #Moving forward left 
#     if xAxis == 65535 and yAxis >= 304 and yAxis < 65535:
#         ledRed2.on()
#         ledRed.off()
#         ledGreen2.off()
#         ledGreen.off()
#         ledYellow.off()
        
#     #Moving backward right
#     if xAxis >= 304 and xAxis < 65535 and yAxis == 65535:
#         ledRed2.off()
#         ledRed.off()
#         ledGreen2.off()
#         ledGreen.on()
#         ledYellow.on()
    
#     #Moving backward left
#     if xAxis >= 304 and xAxis < 65535 and yAxis >= 304 and yAxis < 65535:
#         ledRed2.off()
#         ledRed.on()
#         ledGreen2.off()
#         ledGreen.off()
#         ledYellow.off()

    
#     #Still
#     if xAxis > 47000 and xAxis < 49000 and yAxis > 49000 and yAxis < 51000:
#         ledRed2.off()
#         ledRed.off()
#         ledGreen2.off()
#         ledGreen.off()
#         ledYellow.off()
        
#     #Top Right X-65535 Y-304-65535
#     #Top Left X-65535 Y-65535
#     #Bottom Left X-304-65535 Y-304-50000
#     #Bottom Right X-304-65535 Y-65535

        
