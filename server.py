#!/usr/bin/python3

import socket
import sys

BUF_SIZE = 172
HOST = '10.21.75.71'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((HOST, PORT))
sock.listen(1)
print('Server:', sock.getsockname())
dictionary = { }
while True:
    sc, sockname = sock.accept()
    print('Client:', sc.getpeername())

    try:
        data = sc.recv(BUF_SIZE)
        result = data.decode(encoding='UTF-8', errors='strict').strip()
        header = result[:3]
        key = result[3:11:1]

        if header == 'PUT':
            message = result[11:]
            if len(message) > 160:
                print('Error: message exceeds 160 bytes')
                raise Exception('')

            dictionary[key] = message
            put = 'OK\n'
            data = put.encode()
            print('OK')

        elif header == 'GET':
            get = 'Key: ' + key + ' Message: ' + dictionary[key] + '\n'
            data = get.encode()
            print('Key:', key, 'Message:', dictionary[key])

        else:
            print('Error: must be GET or PUT')
            raise Exception('')
            
    except Exception as err:
        error = 'NO\n'
        data = error.encode()
        print(err)

    sc.sendall(data)
    sc.close()

