from libcamera import Transform
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import PyavOutput

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(
    main={"size": (1920, 1080)},
    controls={"FrameRate": 30},
    transform=Transform(vflip=1)
))

encoder = H264Encoder(bitrate=4000000, repeat=True, iperiod=30, framerate=30)
output = PyavOutput("udp://192.168.10.1:5696?pkt_size=1316", format="mpegts")

picam2.start_recording(encoder, output)
input("Streaming — press Enter to stop\n")
picam2.stop_recording()