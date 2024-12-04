from picamera2 import Picamera2
import time
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

def record_video(output_file, duration):
    # Initialise the Picamera2 instance
    picam2 = Picamera2()

    # Configure the camera for video recording
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)
    encoder = H264Encoder(10000000)
    output = FfmpegOutput(output_file)
   # Start recording
    picam2.start_recording(encoder, output)
    time.sleep(duration)
    picam2.stop_recording()
    picam2.close()

if __name__ == "__main__":
	# Record a 5-second video 
	record_video("./week10-lab2/images/output.mp4", 5)
