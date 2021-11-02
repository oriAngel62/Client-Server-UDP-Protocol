import socket
import sys
from typing import BinaryIO

FOO_PORT = int(sys.argv[1])
FOO_IP = sys.argv[2]
textinfo = str(sys.argv[3])

f = open(textinfo, "rb")
# print(f.read())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

chunckSize = 100

stringFile = f.read()
#file is to big
if len(stringFile) > 50000:
    print("file is to big")
else:
    # print(len(stringFile))
    # listChuncks = []
    # for i in range(0, len(stringFile), chunckSize):
    #     listChuncks.append(stringFile[i:i + chunckSize])
    # #send the chuncks of data to foo
    # for chuncks in listChuncks:
    #     s.sendto(chuncks, (FOO_IP, FOO_PORT))
    # print(len(listChuncks[1]))
    # s.settimeout(8.0)
    s.sendto(stringFile, (FOO_IP, FOO_PORT))
    data, addr = s.recvfrom(1024)
f.close()
s.close()
