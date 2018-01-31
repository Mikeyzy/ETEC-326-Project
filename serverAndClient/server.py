#!python3

import socket, sys, time, threading

cfgFileName = 'server.cfg'

threadList = []
clientIDList = []
clientPWList = []

portRecive = None
portControl = None

def readCFG():
    global portRecive, portControl
    cfgFile = open(cfgFileName, 'r')
    temp = cfgFile.readline()
    portRecive = int(temp[3:temp.index(';')])
    temp = cfgFile.readline()
    portControl = int(temp[3:temp.index(';')])
    cfgFile.close()

def createCFG():
    cfgFile = open(cfgFileName, 'w')
    cfgFile.write("PR=27001;      Recive Client Port, DO NOT change unless you know what you are doing\n")
    cfgFile.write("PC=27002;      Control Client Port, DO NOT change unless you know what you are doing\n")
    cfgFile.write("do not change the order, format: XX=xxxx;comment\n")
    cfgFile.close()

class controlObject:
    def __init__(self, reciverID, reciverPW):
        self.lt = 0.0       #left track
        self.rt = 0.0       #right track
        self.ch = 0.0       #camera horizontal
        self.cv = 0.0       #camera vertical
        self.reciverID = reciverID
        self.reciverPW = reciverPW
    def update(targetID, targetPW, ltrack=0.0, rtrack=0.0, chorizontal=0.0, cvertical=0.0, maxlt=1.0, maxrt=1.0, csensitivity=100):
        if self.reciverID == targetID and self.reciverPW == targetPW:
            self.lt = ltrack * maxlt            #left track
            self.rt = rtrack * maxrt            #right track
            if self.ch + chorizontal <= -1.0:
                self.ch = -1.0
            elif self.ch + chorizontal >= 1.0:
                self.ch = 1.0
            else:
                self.ch += chorizontal * csensitivity / 1000  #camera horizontal
            if self.cv + cvertical <= -1.0:
                self.cv = -1.0
            elif self.cv + cvertical >= 1.0:
                self.cv = 1.0
            else:
                self.cv += cvertical * csensitivity / 1000    #camera vertical
    

listClientR = []
listThreadR = []

class threadConnectionR (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._IR = True
    def run(self, conObj):
        
        data = conObj.recv(256).decode('ascii')

        while _IR:
            

class threadSockR (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._IR = True
    def run(self):
        sockR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverAddressR = ('0.0.0.0', portRecive)
        sockR.bind(serverAddressR)
        sockR.listen(1)
        while _IR:
            conn, clientIP = sock.accept()
            listClientR.append(conn)
            reciveThread = threadConnectionR()
            listThreadC.append(reciveThread)
            reciveThread.run(conn)
            

listClientC = []
listThreadC = []
        
class threadSockC (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global _IR
        while _IR:
            pass

def main():
    # Create a TCP/IP socket
    sockR, sockC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    
    serverAddressC = ('0.0.0.0', portControl)
    print('Starting server, Recive Client Port:', portRecive, 'Control Client Port:', portControl)
    
    sockC.bind(serverAddressC)

    # Listen for incoming connections
    
    sockC.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            dataTotal = b''
            # Receive the data in small chunks and retransmit it
            data = connection.recv(256)
            print(data)
            if data == b'id=123456, pw=abcdef':
                respond = b'test data, var1=11, var2=22, var3=33, var4=44'
                connection.sendall(respond)
                while True:
                    x = bytearray(input('input: '),'ascii')
                    connection.sendall(x)
                    if x == b'quit':
                        break
            else:
                respond = b'test data, invalid id or password'
                connection.sendall(respond)
        finally:
            # Clean up the connection
            connection.close()
