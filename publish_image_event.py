from sense_hat import SenseHat
import paho.mqtt.client as mqtt
from urllib.parse import urlparse
from datetime import datetime
from picamera2 import Picamera2

# Initialize the SenseHAT and MQTT settings
sense = SenseHat()
IMAGE_PATH = "./week10-lab2/images/sensehat_image.jpg"

# Parse MQTT URL for connection details
URL = urlparse("mqtt://broker.emqx.io:1883/lark02/home/cameras/cam1")
BASE_TOPIC = URL.path[1:]

# MQTT event callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print(f"Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message ID: {mid} published successfully")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")
    if rc != 0:
        print("Unexpected disconnection. Reconnecting...")
        client.reconnect()

# Initialize MQTT client
mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# Check for username and password in the URL (none in this basic example)
if URL.username:
    mqttc.username_pw_set(URL.username, URL.password)

# Connect to the MQTT broker
mqttc.connect(URL.hostname, URL.port)
mqttc.loop_start()

# Camera initialization
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

def capture_image(image_path):
    """Capture an image and save it to the specified path."""
    try:
        picam2.start()
        picam2.capture_file(image_path)
        print(f"Image saved to {image_path}")
    finally:
        picam2.stop()

def publish_message():
    """Function to publish the message to the MQTT topic"""
    current_time = datetime.now()
    message = f"Photo taken at {current_time:%H:%M}"
    mqttc.publish(BASE_TOPIC, message)
    print("Message published:", message)

def button_pressed(event):
    """Callback function for SenseHAT button press"""
    if event.action == "pressed":
        try:
            capture_image(IMAGE_PATH)
            print("Image captured using SenseHAT button!")
            publish_message()
        except Exception as e:
            print(f"An error occurred: {e}")

# Set the middle button press to trigger image capture and message publish
sense.stick.direction_middle = button_pressed
print("Press the button on the SenseHAT to capture an image.")

# Keep the script running to detect button presses
import time
while True:
    time.sleep(1)  # Prevent high CPU usage and allow detection of button presses
