import socket
import sys
try:
    SERVER_PORT = int(sys.argv[1])
except:
    quit()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', SERVER_PORT))
setOfChuncks = set()
lastPackage = ''
while True:
    data, addr = s.recvfrom(1024)
    if data not in setOfChuncks:
        print(data[3:].decode(), end='')
        setOfChuncks.add(data)
    s.sendto(data, addr)
