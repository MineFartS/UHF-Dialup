from kiss import encode_kiss_frame, build_ax25_frame
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8100))

def build_frame():
    ax25_frame = build_ax25_frame(
    source="NOCALL",
    dest="APRS",
    info=b"Message-123",
    dest_ssid=0,
    src_ssid=0
)

ax25_frame = build_ax25_frame(
    source="NOCALL",
    dest="APRS",
    info=b"Message-123",
    dest_ssid=0,
    src_ssid=0
)

payload = encode_kiss_frame(ax25_frame, port=0)

s.send(payload)

print("Packet sent to modem!")
