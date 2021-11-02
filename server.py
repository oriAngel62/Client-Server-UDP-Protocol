import socket
import sys

SERVER_PORT = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', SERVER_PORT))
while True:
    # s.settimeout(8.0)
    data, addr = s.recvfrom(1024)
    # sock.settimeout(None)
    print(str(data), addr)
    s.sendto(data, addr)
