from libcamera import Transform
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (1280, 720)},
    controls={"FrameRate": 30},
    transform=Transform(vflip=1)
))

# repeat=True resends stream headers so a viewer can join at any time
# iperiod=15 sends a full keyframe every 15 frames (every half second at 30 fps)
encoder = H264Encoder(bitrate=8000000, repeat=True, iperiod=30)
output = FfmpegOutput("-f mpegts udp://192.168.10.1:5696?pkt_size=1316")

picam2.start_recording(encoder, output)
input("Streaming — press Enter to stop\n")
picam2.stop_recording()