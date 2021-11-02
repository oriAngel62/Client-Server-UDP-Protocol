from datetime import date, time
import socket
import sys
from typing import BinaryIO

FOO_PORT = int(sys.argv[1])
FOO_IP = sys.argv[2]
textinfo = str(sys.argv[3])

f = open(textinfo, "rb")
# print(f.read())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

chunckSize = 6

stringFile = f.read()
#file is to big
if len(stringFile) > 50000:
    print("file is to big")
else:
    print(len(stringFile))
    listChuncks = []
    for i in range(0, len(stringFile) - 1, chunckSize):
        listChuncks.append(stringFile[i:i + chunckSize])
    #send the chuncks of data to foo
    packageNum = 0
    s.settimeout(0.1)
    for chuncks in listChuncks:
        while True:
            try:
                s.sendto(
                    str(packageNum).zfill(3).encode() + chuncks,
                    (FOO_IP, FOO_PORT))
                data, addr = s.recvfrom(1024)
                print("yes")
                break
            except socket.timeout:
                print("no")

        print(data)
        packageNum = packageNum + 1

f.close()
s.close()
