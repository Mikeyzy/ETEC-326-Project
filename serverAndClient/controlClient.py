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

_Connected = False

def debug(*args, sep=' ', end='\n'):
    if _DEBUG:
        print(*args, sep=sep, end=end)

def readCFG():
    global targetID, targetPW, serverAddress, serverPort
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
    global targetID, targetPW
    cfgFile = open(cfgFileName, 'w')
    cfgFile.write('ID=' + targetID + ";\n")
    cfgFile.write('PW=' + targetPW + ";\n")
    cfgFile.write("SA=" + serverAddress + ";\n")
    cfgFile.write("SP=" + serverPort + ";\n")
    cfgFile.close()

def createCFG():
    cfgFile = open(cfgFileName, 'w')
    cfgFile.write('ID=' + str(randint(10,999999)) + ";\n")
    cfgFile.write('PW=' + str(randint(100000,999999)) + ";\n")
    cfgFile.write("SA=127.0.0.1;\n")
    cfgFile.write("SP=27002;\n")
    cfgFile.close()

def setPW():
    global targetID, targetPW
    targetID = input('Target ID: ')
    targetPW = input('Target PW: ')
    writeCFG()

def connect():
    if _Connected:
        pass
    else:
        thrdSock = threadSock()


def main():


class threadSock (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._IR = True
    def run(self):
        global serverAddress, serverPort, targetID, targetPW, _Connected
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        credential = 'controller;'+targetID+';'+targetPW
        rawData = bytearray(credential,'ascii')
        try:
            self.sock.connect(serverAddress, serverPort)
            self.sock.sendall(rawData)
            rawData = self.sock.recv(256)
            dataR = rawData.decode('ascii')
            if '#usedIDError#' in dataR:
                debug('This ID is already in use or not exist.')
                self.sock.close()
            if dataRecived != 'accept':
                debug('host rejected the connection')
                print(dataRecived)
                self.sock.close()
        except Exception:
            #raise(Exception)
            debug('failed to connect to the host')
        else:
            debug('accepted')
            _Connected = True
            while self._IR:
                
                rawData = self.sockR.recv(256)
                dataR = rawData.decode('ascii')
                debug(dataR)
            self.sockR.close()
            _Connected = False

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

if __name__ == "__main__":
    main()
