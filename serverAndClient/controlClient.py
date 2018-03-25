#!python3

import socket, sys, pyglet, time

listKeyName = ['A', 'B', 'X', 'Y', 'L', 'R', 'Select', 'Start', 'StickL', 'StickR', 'DpadX', 'DpadY', 'AxisX', 'AxisY', 'AxisZ', 'RAxisX', 'RAxisY']
listKeyState = [False, False, False, False, False, False, False, False, False, False, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0]

cfgFileName = 'control.cfg'

targetID = None
targetPW = None
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
    targetID = temp[3:temp.index(';')]
    temp = cfgFile.readline()
    targetPW = temp[3:temp.index(';')]
    temp = cfgFile.readline()
    serverAddress = temp[3:temp.index(';')]
    temp = cfgFile.readline()
    serverPort = int(temp[3:temp.index(';')])
    cfgFile.close()

def writeCFG():
    cfgFile = open(cfgFileName, 'w')
    cfgFile.write('ID=' + targetID + ";\n")
    cfgFile.write('PW=' + targetPW + ";\n")
    cfgFile.write("SA=" + serverAddress + ";\tServer Address, NO SPACE\n")
    cfgFile.write("SP=" + serverPort + ";\t\tServer Port, DO NOT change unless you know what you are doing\n")
    cfgFile.write("do not change the order, format: XX=xxxx;comment\n")
    cfgFile.close()

def createCFG():
    cfgFile = open(cfgFileName, 'w')
    cfgFile.write('ID=' + str(randint(10,999999)) + ";\n")
    cfgFile.write('PW=' + str(randint(100000,999999)) + ";\n")
    cfgFile.write("SA=127.0.0.1;  Server Address, NO SPACE\n")
    cfgFile.write("SP=27002;      Server Port, DO NOT change unless you know what you are doing\n")
    cfgFile.write("do not change the order, format: XX=xxxx;comment\n")
    cfgFile.close()

def setPW():
    targetID = input('Target ID: ')
    targetPW = input('Target PW: ')
    writeCFG()

class threadSock (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._IR = True
    def run(self):
        global serverAddress, serverPort
        self.sockR = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverAddressR = (serverAddress, serverPort)
        credential = 'controller;'+targetID+';'+targetPW
        data = bytearray(credential,'ascii')
        try:
            self.sockR.connect(serverAddressR)
            self.sockR.sendall(data)
            rawData = self.sockR.recv(256)
            dataRecived = rawData.decode('ascii')
            if dataRecived != 'accept':
                debug('host rejected the connection')
                print(dataRecived)
                self.sockR.close()
        except Exception:
            #raise(Exception)
            debug('failed to connect to the host')
            time.sleep(10)
            continue
        debug('accepted')
        while self._IR:
            rawData = self.sockR.recv(256)
            dataRecived = rawData.decode('ascii')
            debug('recived:',dataRecived)
        self.sockR.close()

class threadJoystick (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        joystickList = pyglet.input.get_joysticks()

        for i in joystickList:
            try:
                print(i.device, end=", ID ")
            except:
                print(i.name, end=", ID ")
            print(joystickList.index(i))

        joystick = joystickList[int(input('Enter device ID: '))]

        win = pyglet.window.Window(width=640, height=480, caption='Key2Joy Key Config')
        