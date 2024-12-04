from picamera2 import Picamera2
from sense_hat import SenseHat
import os

# Initialize the Sense HAT and Camera at the start
sense = SenseHat()
picam2 = Picamera2()

# Configure the camera
picam2.configure(picam2.create_still_configuration())

# Image save path
IMAGE_PATH = "./week10-lab2/images/button_image.jpg"

def button_pressed(event):
    if event.action == "pressed":
        print("Button pressed! Capturing image...")
        try:
            # Start the camera, capture image, and stop it
            picam2.start()  # Start the camera
            picam2.capture_file(IMAGE_PATH)  # Capture and save the image
            print(f"Image saved to {IMAGE_PATH}")
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            picam2.stop()  # Ensure the camera is properly stopped

# Assign the callback function to the joystick press
sense.stick.direction_middle = button_pressed

print("Press the middle button on the Sense HAT to capture an image.")

# Keep the script running
while True:
    pass