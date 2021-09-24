#!/usr/bin/python3

import socket
import sys

BUF_SIZE = 164
HOST = '10.21.75.71'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
print('Server:', sock.getsockname())
while True:
    sc, sockname = sock.accept()
    print('Client:', sc.getpeername())
    data = sc.recv(BUF_SIZE)
    result = data.decode(encoding='UTF-8', errors='strict')
    print('Recieved',result[:-1])
    sc.sendall(data)
    sc.close()

