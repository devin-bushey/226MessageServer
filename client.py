#!/usr/bin/env python3

import asyncio
import sys
import random
import string

GET_CMD = "GET".encode('utf-8')
PUT_CMD = "PUT".encode('utf-8')
KEY_LENGTH = 8

def validateArguments(args):
    if len(sys.argv) != 4:
        print(f'{sys.argv[0]} needs 3 arguments to transmit')
        sys.exit(-1)

    key = args[3]
    if validateKey(key) == False:
        print('Invalid Key')
        sys.exit(-1)
    
def validateKey(key):
    if key.isdigit() == False:
        return False

    if len(key) != KEY_LENGTH:
        return False

    return True

async def sendRequest(cmd, key, msg):
    reader, writer = await asyncio.open_connection(SERVER_IP, PORT)
    key_msg = cmd + key.encode('utf-8') + msg.encode('utf-8') + b'\n'
    writer.write(key_msg)
    data = await reader.readline()
    #print(f'Recieved: {data.decode("utf-8")}')
    writer.close()
    await writer.wait_closed()
    return data.decode('utf-8')

async def client(key):
    get_result = await sendRequest(GET_CMD, key, '')
    msg = get_result.strip()
    
    if len(msg.strip()) > 0:
        next_key = ''.join(random.choices(string.digits, k=KEY_LENGTH))
        print(f'Message: {msg}')
    else:
        next_key = key

    new_msg = input(f'Please enter a message for key {next_key}: ')
    print('')
    
    # Used this if/else block to remove the empty character in front of the first sent message
    if len(msg.strip()) > 0:
        full_message = msg.strip() + ' ' + new_msg
    else:
        full_message = new_msg

    await sendRequest(PUT_CMD, next_key, new_msg)
    await sendRequest(PUT_CMD, key, full_message)

    
    
    #print(f'Full Message for key {key}: {full_message}')


#
# Main
#
validateArguments(sys.argv)
SERVER_IP = sys.argv[1]
PORT = sys.argv[2]

asyncio.run(client(sys.argv[3]))



