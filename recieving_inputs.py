import paho.mqtt.client as mqtt
import re
from PIL import Image, ImageDraw
import base64
from io import BytesIO
import time 

# --- Create a blank image ---
width, height = 400, 400

# Joystick raw range is around 304 to 65535.
# The neutral/center position is around x=48000 and y=50000.
CENTER_X = 48000
CENTER_Y = 50000
JOYSTICK_MIN = 304
JOYSTICK_MAX = 65535


def normalize_joystick_to_image(xAxis, yAxis, image_width, image_height):
    """Convert raw joystick values into centered image coordinates.
    Center (neutral position) becomes (0, 0).
    """
    xOffset = xAxis - CENTER_X
    yOffset = CENTER_Y - yAxis

    # Scale the offset to the image size.
    # Full stick movement is around 47000..65535 left/right and 49000..65535 up/down.
    scale_x = image_width / 2 / 18000
    scale_y = image_height / 2 / 18000

    xImg = int(xOffset * scale_x)
    yImg = int(yOffset * scale_y)

    return xImg, yImg

MQTT_BROKER = "mqtt-dashboard.com"

ADAFRUIT_AIO_USERNAME = "Izzy0234"

MQTT_ADA_BROKER = "io.adafruit.com"

TOPIC_ADA_JOYSTICK = "Izzy0234/feeds/joystick.joystickcontroller"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to {MQTT_BROKER} with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("TAFE/i-hess/joystick-outputs")

def on_message(client, userdata, msg):
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

    # Convert joystick values into image coordinates before checking direction.
    xImg, yImg = normalize_joystick_to_image(xAxis, yAxis, width, height)
    
    if xImg == -3 and yImg == 3:
        print("Still")
        my_image = drawImage(xAxis, yAxis)
        mqttc_ada.publish("Izzy0234/feeds/joystick.joystickcontroller", my_image)
        print(xImg, yImg)
    # Center / still
    # if xAxis > 47000 and xAxis < 49000 and yAxis > 49000 and yAxis < 51000:
    #     print("Still")
    #     my_image = drawImage(xAxis, yAxis)
    #     mqttc_ada.publish("Izzy0234/feeds/joystick.joystickcontroller", my_image)
    #     print(xImg, yImg)

    # Forward
    elif xImg == 194 and yImg == -172:
    # elif yAxis >= 65500:
        print("Forward")
        my_image = drawImage(xAxis, yAxis)
        mqttc_ada.publish("Izzy0234/feeds/joystick.joystickcontroller", my_image)
        print(xImg, yImg)

    # Backward
    elif xImg == -3 and yImg == 151:
    # elif yAxis <= 500:
        print("Backward")
        my_image = drawImage(xAxis, yAxis)
        mqttc_ada.publish("Izzy0234/feeds/joystick.joystickcontroller", my_image)
        print(xImg, yImg)

    # Left
    elif xImg == 194 and yImg == -172:
    # elif xAxis >= 65500:
        print("Left")
        my_image = drawImage(xAxis, yAxis)
        mqttc_ada.publish("Izzy0234/feeds/joystick.joystickcontroller", my_image)
        print(xImg, yImg)

    # Right
    elif xImg == -529 and yImg == -172:
    # elif xAxis <= 500:
        print("Right")
        my_image = drawImage(xAxis, yAxis)
        mqttc_ada.publish("Izzy0234/feeds/joystick.joystickcontroller", my_image)
        print(xImg, yImg)

# The callback for when the client receives a CONNACK response from the server.
def on_connect_ada(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe("TAFE/i-hess/joystick-outputs")
    
def on_message_ada(client, userdata, msg):
    pass    

# Forward - Y 65535
# Backward - Y 304
# Left - X 65535
# Right - X 304


def drawImage(xAxis, yAxis):
    width, height = 300, 300

    x, y = normalize_joystick_to_image(xAxis, yAxis, width, height)

    # Center is (0,0), so translate to image coordinates with the center at the middle.
    x = x + width // 2
    y = y + height // 2

    # clamp to image bounds
    x = max(0, min(width - 1, x))
    y = max(0, min(height - 1, y))

    img = Image.new("RGB", (width, height), color="purple")
    draw = ImageDraw.Draw(img)
    radius = 12
    draw.ellipse((x - radius, y - radius, x + radius, y + radius),
                 outline="red", fill="yellow", width=4)

    buffer = BytesIO()
    img.save(buffer, format="png")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.connect(MQTT_BROKER)


mqttc_ada = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc_ada.on_connect = on_connect_ada
mqttc_ada.on_message = on_message_ada
mqttc_ada.username_pw_set(ADAFRUIT_AIO_USERNAME, ADAFRUIT_AIO_KEY)
mqttc_ada.connect(MQTT_ADA_BROKER)

mqttc.loop_start()
mqttc_ada.loop_start()
while True:
    time.sleep(3) 
