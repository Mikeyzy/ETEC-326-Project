#!python3

import socket, sys, time, threading

cfgFileName = 'server.cfg'

threadList = []

ServerPort = None

def readCFG():
    global portRecive, portControl
    cfgFile = open(cfgFileName, 'r')
    temp = cfgFile.readline()
    ServerPort = int(temp[11:temp.index(';')])
    cfgFile.close()

def createCFG():
    cfgFile = open(cfgFileName, 'w')
    cfgFile.write("ServerPort=27001;\n")
    cfgFile.close()

def main():
    try:
        readCFG()
    except:
        createCFG()
        readCFG()

    timerThread = timer()
    timerThread.start()
    threadList.append(timerThread)
    reciverProcesser = threadSockR()
    reciverProcesser.start()
    try:
        while True:
            pass
    except:
        for i in threadList:
            i._IR = False


class reciverObject:
    def __init__(self, reciverID, reciverPW, connection):
        self.lt = 0.0       #left track
        self.rt = 0.0       #right track
        self.ch = 0.0       #camera horizontal
        self.cv = 0.0       #camera vertical
        self.ltMax = 0.0
        self.rtMax = 0.0
        self.cSens = 1.0
        self.inUse = False
        self.ID = reciverID
        self.PW = reciverPW
        self.Connection = connection
    def connect(self, reciverID, reciverPW):
        if self.ID == reciverID && self.PW == reciverPW:
            return True
        else:
            return False
    def set(self, lmax, rmax, sens):
        self.ltMax = lmax
        self.rtMax = rmax
        self.cSens = sens
    def updateTrack(self, ltrack=0.0, rtrack=0.0):
        self.lt = ltrack * maxlt            #left track
        self.rt = rtrack * maxrt            #right track
    def updateCamera(self, chorizontal=0.0, cvertical=0.0):
        sens = self.cSens / 10.0
        if self.ch + chorizontal*sens <= -1.0:
            self.ch = -1.0
        elif self.ch + chorizontal*sens >= 1.0:
            self.ch = 1.0
        else:
            self.ch += chorizontal * sens  #camera horizontal

        if self.cv + cvertical*sens <= -1.0:
            self.cv = -1.0
        elif self.cv + cvertical*sens >= 1.0:
            self.cv = 1.0
        else:
            self.cv += cvertical * sens    #camera vertical
    def getState(self):
        return str(self.lt)+';'+str(self.rt)+';'+str(self.ch)+';'+str(self.cv)

class timer (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._IR = True
        self.sendTimer = 0
    def run(self):
        while self._IR:
            self.sendTimer += 1
            time.sleep(1/1000.0)

class threadConnectionR (threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self._IR = True
        self.conn = connection
    def run(self):
        rawData = self.conn.recv(256)
        data = rawData.decode('ascii')
        dataList = data.split(';')
        if dataList[0] == 'reciver':
            reciverID = dataList[1]
            reciverPW = dataList[2]
            self.conn.sendall(b'accept')
        self.conn.sendall(b'accept')
        while self._IR:
            data = input('input:')
            rawData = bytearray(data, 'ascii')
            self.conn.sendall(rawData)

        self.conn.close()

class threadSock (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self._IR = True
        self.reciverIDList = []
        self.reciverObjectList = []

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverAddress = ("0.0.0.0", serverPort)
        self.sock.bind(serverAddress)
        self.sock.listen(1)
        while self._IR:
            conn, clientIP = self.sock.accept()
            try:
                rawData = conn.recv(1024)
                data = rawData.decode('ascii')
                if 'reciver' in data:
                    tempList = data.split(';')
                    if tempList[1] in self.reciverIDList:
                        conn.sendall(bytearray('This ID is already connected. #idused','ascii'))
                        conn.close()
                    else:
                        self.reciverIDList.append(tempList[1])
                        tempObject = reciverObject(tempList[1],tempList[2],conn)
                        self.reciverObjectList.append(tempObject)
                        conn.sendall(bytearray('accept','ascii'))
                elif 'controller' in data:
                    pass
                else:
                    conn.sendall(bytearray('Connection Refused','ascii'))
                    conn.close()
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
