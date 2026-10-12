import signal
import time

from libcamera import Transform
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import PyavOutput

#Settings
WIDTH, HEIGHT = 1920, 1080
FPS = 30
BITRATE = 8_000_000 
KEYFRAME_INTERVAL = 30
MEDIAMTX_URL = "rtsp://127.0.0.1:8554/spuds_cam"

def handle_stop(signum, frame):
    raise SystemExit
signal.signal(signal.SIGTERM, handle_stop)

#Camera
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (WIDTH, HEIGHT)},
    controls={"FrameRate": FPS},
    #transform=Transform(vflip=1)
))

#Encoder
encoder = H264Encoder(
    bitrate=BITRATE,
    repeat=True,
    iperiod=KEYFRAME_INTERVAL,
    framerate=FPS
)

#Output
output = PyavOutput(MEDIAMTX_URL, format="rtsp")

picam2.start_recording(encoder, output)
print(f"Streaming {WIDTH}x{HEIGHT} @ {FPS} fps to {MEDIAMTX_URL}. Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)            # keep the script alive; the stream runs in the background
except (KeyboardInterrupt, SystemExit):
    pass
finally:
    picam2.stop_recording()     # always release the camera, even after an error
    print("Stopped.")