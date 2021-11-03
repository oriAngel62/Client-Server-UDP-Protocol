import socket
import sys

#not enough arguments
try:
    FOO_PORT = int(sys.argv[1])
    FOO_IP = sys.argv[2]
    textinfo = str(sys.argv[3])
except:
    quit()
# file is not exist"
try:
    f = open(textinfo, "rb")
except:
    quit()

stringFile = f.read()
#file is to big
if len(stringFile) > 50000:
    f.close()
    quit()
else:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # size of package up to 100 (97+3 size of package num)
    chunckSize = 97
    listChuncks = []
    for i in range(0, len(stringFile) - 1, chunckSize):
        listChuncks.append(stringFile[i:i + chunckSize])
    #send the chuncks of data to foo
    packageNum = 0
    s.settimeout(0.01)
    for chuncks in listChuncks:
        while True:
            try:
                s.sendto(
                    str(packageNum).zfill(3).encode() + chuncks,
                    (FOO_IP, FOO_PORT))
                data, addr = s.recvfrom(1024)
                break
            except socket.timeout:
                continue
        packageNum = packageNum + 1
f.close()
s.close()
