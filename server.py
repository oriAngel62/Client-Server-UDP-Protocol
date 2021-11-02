from datetime import date
import socket
import sys

SERVER_PORT = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', SERVER_PORT))
# s.settimeout(0.5)
# while True:
#     try:
#         data, addr = s.recvfrom(1024)
#         print(data[:3].decode())
#         print(str(data), addr)
#         # s.settimeout(8.0)
#         while True:
#             s.sendto(b"y", addr)
#             break
#     except socket.timeout:
#         continue

while True:
    data, addr = s.recvfrom(1024)
    print(data[:3].decode())
    print(str(data), addr)
    s.sendto(data, addr)
