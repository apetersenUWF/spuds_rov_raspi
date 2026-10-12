from libcamera import Transform
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (1920, 1080)},
    controls={"FrameRate": 24},
    transform=Transform(vflip=1)
))

encoder = H264Encoder(bitrate=4000000, repeat=True, iperiod=30, framerate = 24)
output = FfmpegOutput("-f mpegts udp://192.168.10.1:5696?pkt_size=1316")
#output = FfmpegOutput("test.mp4")
picam2.start_recording(encoder, output)
input("Streaming — press Enter to stop\n")
picam2.stop_recording()