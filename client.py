#!/usr/bin/env python3

import asyncio
import sys
import random
import string
import traceback

GET_CMD = "GET".encode('utf-8')
BLANK = ''
PUT_CMD = "PUT".encode('utf-8')
KEY_LENGTH = 8
NO_RESPONSE = 'NO'

#
# PURPOSE:
# Given an array of command line arguments, validate whether there are the correct number of arguments
# and validate the key input 
#
# PARAMETERS:
# 'args' is the array of command line arguments used when running the program
#
# RETURN/SIDE EFFECTS:
# Terminates the program if validation fails
#
# NOTES:
# IP address and port arguments are not validated
#
def validateArguments(args):
    if len(sys.argv) != 4:
        print(f'{sys.argv[0]} needs 3 arguments to transmit')
        sys.exit(-1)

    key = args[3]

    if key.isdigit() == False:
        print('Key must be all digits')
        sys.exit(-1)

    if len(key) != KEY_LENGTH:
        print(f'Key length must be {KEY_LENGTH}')
        sys.exit(-1)
    
#
# PURPOSE:
# Given a command, valid key, and message, send the given command with given key and message to the server
# Handles GET or PUT requestsi
#
# PARAMETERS:
# 'cmd' is a string which is assumed to be either a GET or PUT
# 'key' is a string which is the key to be sent to the server
# 'msg' is the associated message for the key. It should be blank if the command is a GET
#
# RETURN/SIDE EFFECTS:
# Returns the decoded response by the server
#
# NOTES:
# Opens/closes a new connection to the server
#

async def sendGetRequest(cmd, key, msg):
    reader, writer = await asyncio.open_connection(SERVER_IP, PORT)
    request = cmd + key.encode('utf-8') + msg.encode('utf-8') + b'\n'
    writer.write(request)
    data = await reader.readline()
    #print(f'Recieved: {data.decode("utf-8")}')
    writer.close()
    await writer.wait_closed()
    return data.decode('utf-8')

async def sendPutRequest(cmd, key, msg):
    check = True
    print(f'key is: ', key)
    reader, writer = await asyncio.open_connection(SERVER_IP, PORT)
    request = cmd + key.encode('utf-8') + msg.encode('utf-8') + b'\n'
    writer.write(request)
    data = await reader.readline()
    writer.close()
    await writer.wait_closed()
        
    while check:
        if data.decode('utf-8')[:len(NO_RESPONSE)] == NO_RESPONSE:
            reader, writer = await asyncio.open_connection(SERVER_IP, PORT)
            key = data.decode('utf-8')[len(NO_RESPONSE):KEY_LENGTH]
            new_msg = key + data.decode('utf-8')[KEY_LENGTH:]
            request = cmd + key.encode('utf-8') + new_msg.encode('utf-8') + b'\n'
            writer.write(request)
            data = await reader.readline()
            print(f'Recieved: {data.decode("utf-8")}')
            writer.close()
            await writer.wait_closed()
        else:
            check = False
        #print(f'Recieved: {data.decode("utf-8")}')
    return data.decode('utf-8')
#
# PURPOSE:
# Given a key from the command line, print all associated messages in the thread, then prompt
# the user for a new message. This new message will be paired with a randomly generated key
# Finally, the new message and key are sent to the server by a PUT request
#
# PARAMETERS:
# 'key' is a string, which is an argument from the commandline.
# Assume the key has been validated as an 8-digit string
#
# NOTES:
# If there is a message returned from the server, assume that meesage consists of
# of an 8-digit key and a message body
#
async def get():
    global key
    while True:
        get_result = await sendGetRequest(GET_CMD, key, BLANK)
        msg = get_result.strip()[KEY_LENGTH:]
        
        while len(msg) > 0:
            key = get_result.strip()[:KEY_LENGTH]
            print(f'Message: {msg}')
            get_result = await sendGetRequest(GET_CMD, key, BLANK)
            msg = get_result.strip()[KEY_LENGTH:]
        
        await asyncio.sleep(5)

async def put():
    global key
    while True:

        next_key = ''.join(random.choices(string.digits, k=KEY_LENGTH))

        loop = asyncio.get_running_loop()
        try:
            new_msg = await loop.run_in_executor(None, input, f'Please enter a message for key {next_key}: ')
        except:
           break
        new_msg = next_key + new_msg

        await sendPutRequest(PUT_CMD, key, new_msg)

async def main():
    try:
        await asyncio.gather(get(), put())
    except Exception as e:
        print(e)
        traceback.print_exc()


validateArguments(sys.argv)
SERVER_IP = sys.argv[1]
PORT = sys.argv[2]
key = sys.argv[3]

asyncio.run(main())

