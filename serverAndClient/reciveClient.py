#!python3

import socket, sys, time, threading, playsound
from random import randint

cfgFileName = 'recive.cfg'

myID = None
myPW = None
serverAddress = None
serverPort = None

_DEBUG = True

def debug(*args, sep=' ', end='\n'):
    if _DEBUG:
        print(*args, sep=sep, end=end)

def readCFG():
    global myID, myPW, serverAddress, serverPort
    cfgFile = open(cfgFileName, 'r')
    temp = cfgFile.readline()
    myID = temp[3:temp.index(';')]
    temp = cfgFile.readline()
    myPW = temp[3:temp.index(';')]
    temp = cfgFile.readline()
    serverAddress = temp[3:temp.index(';')]
    temp = cfgFile.readline()
    serverPort = int(temp[3:temp.index(';')])
    cfgFile.close()

def createCFG():
    cfgFile = open(cfgFileName, 'w')
    cfgFile.write('ID=' + str(randint(10,999999)) + ";\n")
    cfgFile.write('PW=' + str(randint(100000,999999)) + ";\n")
    cfgFile.write("SA=127.0.0.1;  Server Address, NO SPACE\n")
    cfgFile.write("SP=27001;      Server Port, DO NOT change unless you know what you are doing\n")
    cfgFile.write("do not change the order, format: XX=xxxx;comment\n")
    cfgFile.close()

def updateState(commands):
    pass

def readDistance():
    distance = 0
    return distance

def main():
    global myID, myPW
    try:
        readCFG()
    except:
        createCFG()
        readCFG()
    finally:
        debug('initialized with ID', myID, ', password', myPW)

    ConThread = threadSock()
    SoundThread = threadSound()
    ConThread.start()
    SoundThread.start()
    try:
        while True:
            pass
    except:
        ConThread._IR = False

class threadSound (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._IR = True
        self._EN = False
        self.Path = ""
    def run(self):
        while self._IR:
            if self._EN:
                self._EN = False
                try:
                    playsound.playsound(self.Path)
                except:
                    pass
    def play(self, path):
        self.Path = path
        self._EN = True

class threadSock (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._IR = True
    def run(self):
        global serverAddress, serverPort
        self.sockR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverAddressR = (serverAddress, serverPort)
        credential = 'reciver;'+myID+';'+myPW
        data = bytearray(credential,'ascii')
        while self._IR:
            try:
                self.sockR.connect(serverAddressR)
                self.sockR.sendall(data)
                rawData = self.sockR.recv(256)
                dataR = rawData.decode('ascii')
                if '#usedIDError#' in dataR:
                    debug('Same ID already been used.')
                    self.sockR.close()
                    continue
                if 'accept' not in dataR:
                    debug('host rejected the connection')
                    self.sockR.close()
                    continue
            except Exception:
                #raise(Exception)
                debug('failed to connect to the host')
                time.sleep(10)
                continue
            debug('accepted')
            while True:
                rawData = self.sockR.recv(1024)
                dataR = rawData.decode('ascii')
                if '#idle#' in dataR:
                    debug('Idle')
                    dataT = '#ok#'
                    rawData = bytearray(dataT,'ascii')
                else:
                    debug('recived:',dataR)
                    updateState(dataR)
                    dataT = str(readDistance())
                    rawData = bytearray(dataT,'ascii')
                self.sockR.sendall(rawData)
            self.sockR.close()
            break


if __name__ == "__main__":
    main()
