import paho.mqtt.client as mqtt
from urllib.parse import urlparse

# MQTT URL and topic configuration
URL = urlparse("mqtt://broker.emqx.io:1883/lark02/home/cameras/cam1")
BASE_TOPIC = URL.path[1:]

# Event callback definitions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(f"{BASE_TOPIC}/#", qos=1)  # Subscribe to all subtopics
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"Subscribed with QoS {granted_qos[0]}")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")
    if rc != 0:
        print("Unexpected disconnection. Attempting to reconnect...")
        try:
            client.reconnect()
        except Exception as e:
            print(f"Reconnection failed: {e}")


mqttc = mqtt.Client()
# Assign callbacks
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

# Set username and password if provided in the URL
if URL.username:
    mqttc.username_pw_set(URL.username, URL.password)

# Connect to the MQTT broker
mqttc.connect(URL.hostname, URL.port)
mqttc.loop_forever()