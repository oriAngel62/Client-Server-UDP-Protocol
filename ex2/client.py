import socket
import sys
import os
import time
import string
import random
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


SERVER_PORT = 12345 #int(sys.argv[1])
SERVER_IP = '10.0.2.5' #sys.argv[2]
PATH = '/home/david1998/Documents/practice' #sys.argv[3]
SERVER_ADDR = (SERVER_IP, SERVER_PORT)
TIME_TO_REACH_SERVER = 5 #float(sys.argv[4])
NEW_ACCOUNT = False
try:
    ID = sys.argv[5]
except IndexError:
    ID = 1
    NEW_ACCOUNT = True
Windows = False

class Client:

    def MainFolderClone(self,PATH,s):
        mainFolderName = s.recv(100).decode()
        path = os.path.join(PATH, mainFolderName)
        if Windows:
            path = path.replace("/","\\")
        os.mkdir(path)
        hasChildren = s.recv(1024).decode()
        if hasChildren == "0":
            return
        howManySubs = s.recv(1024).decode()
        for fileOrFolder in range(0,howManySubs):
            subName = s.recv(1024).decode()
            Client.recursiveCloneFolder(self,path + subName,s,subName)
# sds
    def randomizePswrd():
        pswd = ''
        for i in range(3):
            pswd += random.choice(string.ascii_letters)
        return pswd



    def recursiveCloneFolder(self,path,s,nameOfSub):
        isFolder = s.recv(100).decode()                        #copy file
        if isFolder == "0":
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
            hasSubFilesOrFolders = s.recv(10).decode()
            if hasSubFilesOrFolders == "0":
                return
            else:
                numOfSubs = s.recv(100).decode()
                for fileOrFolder in range(0,numOfSubs):
                    name = s.recv(1024).decode()
                    Client.recursiveCloneFolder(self,path,s,name)

##########################################################till this line sync to client##################################



    def startSync(self,path,s,pswd):
        while True:
            recvPswd =  s.recv(3).decode()
            if pswd == recvPswd:
                break
        if os.path.isfile(path):
            s.send("0".encode())
            Client.sendingFile(self,s,path)
        else:
            s.send("1".encode())
            if os.path.exists(path):
                print("aigght")
            if Windows:
                dir_list= os.listdir(path)
                path = path + "\\"
            else:
                dir_list = os.listdir(path)
                path = path + "/"
            if (len(dir_list) == 0):
                s.send("0".encode())
                return
            else:
                s.send("1".encode())
                numOfSubs = len(dir_list)
                numOfSubsStr = str(numOfSubs)
                s.send(numOfSubsStr.encode('utf8'))
                time.sleep(1)
                for fileOrFolder in dir_list:
                    paswd = Client.randomizePswrd()
                    s.send(paswd.encode())
                    print(paswd)
                    s.send(fileOrFolder.encode())
                    Client.startSync(self,path + fileOrFolder,s,paswd)
        
            
    
    def sendingFile(self,s,path):
        f= open(path, "rb")
        l = f.read(2048)
        while(l):
            s.send(l)
            l = f.read(2048)
        f.close()

            



meClient = Client()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDR)
print(os.listdir('/home/david1998/Music'))
#time = time()
if ID == 1:
    s.send("0".encode())
    NEW_ACCOUNT = True
else:
    s.send(ID.encode())   
s.send(PATH.encode())
if PATH.find("/") != -1:
    Windows = False
else:
    Windows = True
if NEW_ACCOUNT:
    print("waiting")
    ID = s.recv(128).decode()
    print(ID)
    paswd = Client.randomizePswrd()
    s.send(paswd.encode())
    meClient.startSync(PATH,s,paswd)
else:
    meClient.MainFolderClone(PATH,s)
#clone recursivly the folder from the cloud to the PATH
#sync
#if changes :
 #   s.send(event)

# data = s.recv(100)
# print("Server sent: ", data)
# s.send(b'318572047')
# data = s.recv(100)
# print("Server sent: ", data)
# s.close()
