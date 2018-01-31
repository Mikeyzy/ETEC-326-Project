#!python3

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    # Send data
    message = b'id=123456, pw=abcdef'
    print('sending {!r}'.format(message))
    sock.sendall(message)

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
