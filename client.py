import socket
import sys
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


SERVER_PORT = int(sys.argv[1])
SERVER_IP = sys.argv[2]
PATH = sys.argv[3]
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
TIME_TO_REACH_SERVER = float(sys.argv[4])
NEW_ACCOUNT = False
try:
    ID = sys.argv[5]
except IndexError:
    ID = 1
    NEW_ACCOUNT = True


def MainFolderClone(self,PATH,Windows,s):
    mainFolderName = s.recv(100)
    path = os.path.join(PATH, mainFolderName)
    if Windows:
        path = path.replace("/","\\")
    os.mkdir(path)
    hasChildren = s.recv(1024)
    if hasChildren == False:
        return
    howManySubs = s.recv(1024)
    for fileOrFolder in range(0,howManySubs):
        subName = s.recv(1024)
        recursiveCloneFolder(self,path + subName,Windows,s,subName)



def recursiveCloneFolder(self,path,Windows,s,nameOfSub):
    isFolder = s.recv(100)                        #copy file
    if isFolder == False:
        newPath = os.path.join(path, nameOfSub)
        if Windows:
            newPath = newPath.replace("/","\\")
        f = open(newPath, 'w')                       #creating new file
        l= s.recv(1024)
        while l:
            f.write(l)
            l = s.recv(1024)
        f.close()                            #recursion supose to end here  
        return       
    else:
        newPath = os.path.join(path, nameOfSub)
        if Windows:
            newPath = newPath.replace("/","\\")
        os.mkdir(newPath)
        hasSubFilesOrFolders = s.recv(10)
        if hasSubFilesOrFolders == False:
            return
        else:
            numOfSubs = s.recv(100)
            for fileOrFolder in range(0,numOfSubs):
                name = s.recv(1024)
                recursiveCloneFolder(self,path ,Windows,s,name)


def startSync(self,PATH,s,Windows):


            




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDR)
#time = time()
s.send(ID)
s.send(PATH)
if "/" in PATH:
    Windows = False
else:
    Windows = True
if NEW_ACCOUNT:
    ID = s.recv(128)
    startSync(self,PATH,s,Windows)
else:
    MainFolderClone(set,PATH,Windows,s)
#clone recursivly the folder from the cloud to the PATH
#sync
if changes :
    s.send(event)

data = s.recv(100)
print("Server sent: ", data)
s.send(b'318572047')
data = s.recv(100)
print("Server sent: ", data)
s.close()
