from posix import listdir
import socket
import time 
import sys
import string
import random
import os

Windows =False
MY_PORT = 12345 #int(sys.argv[1])
folderName_dict = {}
path_dict = {}
changes_dict = {}
folder_name = ''



class Server:
    def randomizeSequence():
        # print("here")
        id =''
        for i in range(128):
            b = random.randint(0,1)
            if b == 0:
                id += random.choice(string.ascii_letters)
            else:
                id += str(random.randint(0,9))
        return id





    def sendingFile(self,client_socket,fileName):
        f = open(fileName, "rb")
        l = f.read(1024)
        while (l):
            Server.client_socket.send(l)
            l = f.read(1024)
        f.close()

    def recursiveSync(self,client_socket,path,fileOrFolderName):
        if os.path.isfile(path):
            client_socket.send("0".encode())
            Server.sendingFile(self,client_socket,path)
        else:
            client_socket.send("1".encode())
            dir_list = os.listdir(path + "/")
            if len(dir_list) == 0:
                client_socket.send("0".encode())
            else:
                client_socket.send("1".encode())
                client_socket.send(len(dir_list).encode())
                for fileOrFolder in dir_list:
                    client_socket.send(fileOrFolderName.encode())
                    Server.recursiveSync(self,client_socket,path + "/" + fileOrFolder, fileOrFolder)



    def sync(self,client_socket,PATH):
        mainFolderName = os.path.basename(os.path.normpath(PATH))
        client_socket.send(mainFolderName.encode())
        dir_list = os.listdir(mainFolderName + "/")
        if len(dir_list) == 0:
            client_socket.send("0".encode())
        else:
            client_socket.send("1".encode())
            client_socket.send(len(dir_list).encode())
            for fileOrFolder in dir_list:
                client_socket.send(fileOrFolder.encode())
                Server.recursiveSync(self,client_socket,path_dict[ID] + "/" + fileOrFolder,fileOrFolder)
            
#############################################till this point sync to the client################


    def newClient(self, client_socket,ID,PATH):
        client_socket.send(Server.randomizeSequence().encode())                  #if it's a new client then we :
        psw = client_socket.recv(3).decode()
        client_socket.send(psw.encode())
        folder_name = os.path.basename(os.path.normpath(PATH))   # that's connected to the client
        isFolder = client_socket.recv(1)
        if not isFolder:
            print("went wrong")
        folderName_dict[ID] = folder_name
        cwd = os.getcwd()
        path = os.path.join(cwd, folder_name)
        os.mkdir(path)
        path_dict[ID] = path
        hasChildren = client_socket.recv(1).decode()
        if not hasChildren:
            return
        numOfSubsstr = client_socket.recv(1).decode('utf8')
        numOfSubs = int(numOfSubsstr)
        for fileOrFolder in range(0,numOfSubs):
            pswd = client_socket.recv(3).decode()
            name = client_socket.recv(124).decode()
            Server.syncToCloud(self,path ,client_socket,name , pswd)
    #syncToCloud(self,path,Windows,client_socket,folder_name)
    


    def syncToCloud(self,path,client_socket,nameOfSub, pswd):
        client_socket.send(pswd.encode())
        isFolder = client_socket.recv(1).decode()                        #copy file
        newPath = os.path.join(path, nameOfSub)
        if isFolder == "0":
            if Windows:
                newPath = newPath.replace("/","\\")
            f = open(newPath, 'w')                       #creating new file
            l= client_socket.recv(2048)
            while l:
                try:
                    f.write(l)
                finally:
                    f.write(l.decode('utf-8'))
                l = client_socket.recv(2048)
            f.close()                            #recursion supose to end here  
            return       
        else:
            if Windows:
                newPath = newPath.replace("/","\\")
            os.mkdir(newPath)
            hasSubFilesOrFolders = client_socket.recv(1).decode()
            if hasSubFilesOrFolders == "0":
                return
            else:
                numOfSubs = client_socket.recv(10).decode()
                for fileOrFolder in range(0,int(numOfSubs)):
                    pasword = client_socket.recv(3).decode()
                    name = client_socket.recv(1024).decode()
                    Server.syncToCloud(self,newPath,client_socket,name,pasword)



def checkChange(self, event):
    i=0






meServer = Server()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', MY_PORT))
server.listen(24000)
while True:
    client_socket, client_address = server.accept()
    ID = client_socket.recv(128).decode()
    PATH = client_socket.recv(124).decode()
    print(PATH)
    if PATH.find("/") == -1:
        Windows = True
    # print(Windows)
    if ID == "0":
        print("wentin")
        meServer.newClient(client_socket,ID,PATH)
        print("after ID")
        #sync
    #need to make a condition if the ID is wrong
    else:
        meServer.sync(client_socket,PATH)
    #     for change in changes_dict[ID]:
    #         checkChange(change)
    # monitoring = True
    # while monitoring:
    #     event = client_socket.recv(10024)      #flow
    #     if event == False:
    #         monitoring = False
    #         break
    #     else:
    #         changes_dict[ID].append(event)
    #         checkChange(event)
    client_socket.shutdown(socket.SHUT_WR)



    
    #print('Received: ', data)
    # data = client_socket.recv(20)
    # print('Received: ', data)
    # client_socket.send(data.upper())
    # client_socket.shutdown(socket.SHUT_WR)
    # print('Client disconnected')
