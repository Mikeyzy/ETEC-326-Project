#!python3

import socket, sys
from random import randint

cfgFileName = 'recive.cfg'

myID = None
myPW = None
serverAddress = None
serverPort = None

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

def main():
    global myID, myPW
    try:
        readCFG()
    except:
        createCFG()
        readCFG()
    finally:
        print('initialized with ID', myID, ', password', myPW)
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 5000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    try:
        # Send data
        credential = 'type=reciver,id='+myID+',pw='+myPW
        data = bytearray(credential,'ascii')
        #print('sending {!r}'.format(message))
        sock.sendall(data)

        data = sock.recv(256)
        print(str(data))

        while True:
            data = sock.recv(256)
            print('recived: '+ data.decode('ascii'))
            if data == b'quit':
                break
        
    finally:
        print('closing socket')
        sock.close()

if __name__ == "__main__":
    main()
