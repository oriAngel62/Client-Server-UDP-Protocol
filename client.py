import socket
import sys

FOO_PORT = int(sys.argv[1])
FOO_IP = sys.argv[2]
textinfo = str(sys.argv[3])

f = open(textinfo, "rb")
# print(f.read())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(f.read(), (FOO_IP, FOO_PORT))
data, addr = s.recvfrom(1024)
print(str(data), addr)

f.close()

s.close()
