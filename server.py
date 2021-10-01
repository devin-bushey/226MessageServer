#!/usr/bin/python3

import socket
import sys

BUF_SIZE = 1024
HOST = ''   #empty string = ALL
PORT = 12345
NUM_OF_CONNECTIONS = 1

# PURPOSE:
# Create a TCP Server
# RETURN:
# Returns a socket
def createSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(NUM_OF_CONNECTIONS)
    print('Server:', sock.getsockname())
    return sock

# PURPOSE:
# Validates message length. Must be between 0-160 bytes
# PARAMETERS:
# msg = string
# RETURN:
# bool
def checkMsgLen(msg):
    if (len(msg) <= 0 or len(msg) > 160):
        print('Error: message must be between 0-160 bytes')
        return False
    return True

# PURPOSE:
# Validate GET data. 
# GET request cannot include a message
# Checks if there is a message with the associated key
# PARAMETERS:
# key, message = string
# dictionary = dictionary containing key/value pairs for the key/message
# RETURN:
# bool
def checkGET(key, message, dictionary):
    if (len(message) != 0):
        print('Error: GET cannot include message')
        return False
    if not bool(dictionary.get(key)):
        print('Error: Message not found')
        return False
    return True

# PURPOSE:
# Process the PUT request by validating the data and encoding the success/fail message
# PARAMETERS:
# message = string
# RETURN:
# returns the encoded OK message if data is valid, otherwise raises an exception
def processPUT(message):
    if not checkMsgLen(message):
        raise Exception('NO\n')
    print('OK')
    put = 'OK\n'
    data = put.encode()
    return data

# PURPOSE:
# Process the GET request by validating the data and encoding the message that is assocuated with the key
# PARAMETERS:
# key = string, 8 byte alphanumeric
# message = string, 160 bytes
# dictionary = dictionary containing key/value pairs for the key/message
# RETURN:
# returns the encoded message if data is valid, otherwise raises an exception
def processGET(key, message, dictionary):
    if not checkGET(key, message, dictionary):
        raise Exception('\n')
    print('Key:', key, 'Message:', dictionary[key])
    get = dictionary[key] + '\n'
    data = get.encode()
    return data

# PURPOSE:
# encode an error message
# PARAMETERS:
# err = error message that is created from an Exception
# RETURN:
# return encoded error message
def processError(err):
    err = str(err)
    data = err.encode()
    print(err)
    return data

# PURPOSE:
# Send encoded data to the client and terminate the socket
# PARAMETERS:
# socket = opened socket
# data = encoded data that is ready to be sent to the client
# RETURN
# void
def sendData(socket, data):
    socket.sendall(data)
    socket.close()

# PURPOSE:
# run a basic message server that expects either a PUT or GET command followed by a 8-byte alphanumeric
# key, followed by an optional newline-terminated string (if the command is PUT)
# The PUT command stores the message and its associated key in memory and returns a status message to the client
# The GET command retrieves the message in memory that is associated with the given key and returns it to the client
# PARAMETERS:
# sock contains the socket assocated with the server
# RETURN:
# void
def runBasicMessageServer(sock):
    dictionary = { }
    while True:
        sc, sockname = sock.accept()
        print('Client:', sc.getpeername())

        try:
            data = sc.recv(BUF_SIZE)
            data_decoded = data.decode(encoding='UTF-8', errors='strict').strip()

            header = data_decoded[:3]
            key = data_decoded[3:11]
            message = data_decoded[11:]

            if header == 'PUT':
                data = processPUT(message)
                dictionary[key] = message
            elif header == 'GET':
                data = processGET(key, message, dictionary)
            else:
                print('Error: must be GET or PUT')
                raise Exception('NO\n')
                
        except Exception as err:
            data = processError(err)

        try:
            sendData(sc, data)
        except Exception as err:
            print(err)

def main():
    sock = createSocket()
    runBasicMessageServer(sock)

if __name__ == "__main__":
    main()
