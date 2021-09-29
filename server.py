#!/usr/bin/python3

import socket
import sys

BUF_SIZE = 1024
HOST = ''
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
        key = result[3:11]

        if header == 'PUT':
            message = result[11:]
            if (len(message) <= 0 or len(message) > 160):
                print('Error: message must be between 0-160 bytes')
                raise Exception('NO\n')

            dictionary[key] = message
            put = 'OK\n'
            data = put.encode()
            print('OK')

        elif header == 'GET':
            if (len(result[11:]) != 0):
                print('Error: GET cannot include message')
                raise Exception('\n')
            if bool(dictionary.get(key)) == False:
                raise Exception('\n')

            get = dictionary[key] + '\n'
            data = get.encode()
            print('Key:', key, 'Message:', dictionary[key])

        else:
            print('Error: must be GET or PUT')
            raise Exception('NO\n')
            
    except Exception as err:
        err = str(err)
        data = err.encode()
        print(err)

    try:
        sc.sendall(data)
        sc.close()
    except Exception as err:
        print(err)


