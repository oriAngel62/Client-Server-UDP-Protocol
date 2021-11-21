from posix import listdir
import socket
import time 
import sys
import string
import random
import os


MY_PORT = int(sys.argv[1])
folderName_dict = {}
path_dict = {}
changes_dict = {}
folder_name = ''

def randomizeSequence():
    id =''
    for i in range(128):
        b = random.randint(0,1)
        if b == 0:
            id += random.choice(string.ascii_letters)
        else:
            id += str(random.randint(0,9))

def newClient(self, client_socket,ID,PATH):
    client_socket.send(randomizeSequence())                  #if it's a new client then we :
    folder_name = os.path.basename(os.path.normpath(PATH))   # that's connected to the client
    folderName_dict[ID] = folder_name
    cwd = os.getcwd()
    path = os.path.join(cwd, folder_name)
    os.mkdir(path)
    path_dict[ID] = path
    syncToCloud(self,client_socket,path)


def syncToCloud(self,client_socket,path):




def checkChange(self, event):
    i=0

def sendingFile(self,client_socket,fileName):
    f = open(fileName, "rb")
    l = f.read(1024)
    while (l):
        client_socket.send(l)
        l = f.read(1024)
    client_socket.send(False)
    f.close()

def recursiveSync(self,client_socket,path,fileOrFolderName):
    if os.path.isfile(path):
        client_socket.send(False)
        sendingFile(self,client_socket,fileOrFolderName)
    else:
        client_socket.send(fileOrFolderName)
        dir_list = os.listdir(path + "/")
        if len(dir_list) == 0:
            client_socket.send(False)
        else:
            client_socket.send(True)
            client_socket.send(len(dir_list))
            for fileOrFolder in dir_list:
                client_socket.send(fileOrFolderName)
                recursiveSync(self,client_socket,path + "/" + fileOrFolder, fileOrFolder)



def sync(self,client_socket,ID):
    client_socket.send(folderName_dict[ID])
    dir_list = os.listdir(path_dict[ID] + "/")
    if len(dir_list) == 0:
        client_socket.send(False)
    else:
        client_socket.send(True)
        client_socket.send(len(dir_list))
        for fileOrFolder in dir_list:
            client_socket.send(fileOrFolder)
            recursiveSync(self,client_socket,path_dict[ID] + "/" + fileOrFolder,fileOrFolder)
            





server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', MY_PORT))
server.listen(24000)
while True:
    client_socket, client_address = server.accept()
    ID = client_socket.recv(128)
    PATH = client_socket.recv(1024)
    if ID == 1:
        newClient(client_socket,ID,PATH)
        #sync
    #need to make a condition if the ID is wrong
    else:
        path = path_dict[ID]
        sync(client_socket,ID)
        for change in changes_dict[ID]:
            checkChange(change)
    monitoring = True
    while monitoring:
        event = client_socket.recv(10024)      #flow
        if event == False:
            monitoring = False
            break
        else:
            changes_dict[ID].append(event)
            checkChange(event)
    client_socket.shutdown(socket.SHUT_WR)



    #print('Received: ', data)
    
    data = client_socket.recv(20)
    print('Received: ', data)
    client_socket.send(data.upper())
    client_socket.shutdown(socket.SHUT_WR)
    print('Client disconnected')
