#!python3

import socket, sys, time, threading

cfgFileName = 'server.cfg'

threadList = []

serverPort = None

def readCFG():
    global serverPort
    cfgFile = open(cfgFileName, 'r')
    temp = cfgFile.readline()
    serverPort = int(temp[11:temp.index(';')])
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
    thrdSock = threadSock()
    thrdSock.start()
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
        self.rearDistance = 0.0
        self.ltMax = 0.0
        self.rtMax = 0.0
        self.cSens = 1.0
        self.inUse = False
        self.Name = reciverID
        self.Password = reciverPW
        self.Connection = connection
    def connect(self, reciverID, reciverPW):
        if self.inUse:
            return False
        elif self.Name == reciverID and self.Password == reciverPW:
            self.inUse = True
            self.Connection.settimeout(0.5)
            return True
        else:
            return False
    def disconnect(self):
        self.inUse = False
        self.Connection.settimeout(None)
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

class threadReciver (threading.Thread):
    def __init__(self, reciver, parent):
        threading.Thread.__init__(self)
        self._IR = True
        self.Reciver = reciver
        self.Parent = parent
        self.Connection = reciver.Connection
        self.IDLE = True
    def run(self):
        while self._IR:
            try:
                if self.IDLE:
                    self.Connection.sendall(bytearray('#idle#','ascii'))
                    rawData = self.Connection.recv(1024)
                    time.sleep(2)
                else:
                    dataT = self.Reciver.getState()
                    self.Connection.sendall(bytearray(dataT, 'ascii'))
                    rawData = self.Connection.recv(1024)
                    dataR = rawData.decode('ascii')
                    self.Reciver.rearDistance = float(dataR)
            except TimeoutError:
                debug('Package Lost')
            except ConnectionResetError:
                debug('Connection Lost')
                self.Parent.reciverThreadList.remove(self)
                self.Parent.reciverIDList.remove(self.Reciver.Name)
                self.Parent.reciverObjectList.remove(self.Reciver)
                break

class threadSock (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._IR = True
        self.reciverIDList = []
        self.reciverObjectList = []
        self.reciverThreadList = []
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
                        conn.sendall(bytearray('This ID is already connected. #usedIDError#','ascii'))
                        conn.close()
                    else:
                        self.reciverIDList.append(tempList[1])
                        tempObject = reciverObject(tempList[1],tempList[2],conn)
                        self.reciverObjectList.append(tempObject)
                        conn.sendall(bytearray('accept','ascii'))
                        tempThread = threadReciver(tempObject, self)
                        tempThread.start()
                        self.reciverThreadList.append(tempThread)
                elif 'controller' in data:
                    pass
                else:
                    conn.sendall(bytearray('Connection Refused','ascii'))
                    conn.close()
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
