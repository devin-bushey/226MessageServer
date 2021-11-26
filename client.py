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
# Send a GET request to the server using the latest key 
#
# PARAMETERS:
# 'key' is a string which is the key to be sent to the server.
# key is a global variable because its needed between both PUT and GET's in the main function
#
# RETURN/SIDE EFFECTS:
# Returns the decoded response by the server
#
# NOTES:
# Opens/closes a new connection to the server
#

async def sendGetRequest():
    global key
    reader, writer = await asyncio.open_connection(SERVER_IP, PORT)
    request = GET_CMD + key.encode('utf-8') + b'\n'
    writer.write(request)
    data = await reader.readline()
    #print(f'Recieved: {data.decode("utf-8")}')
    writer.close()
    await writer.wait_closed()
    return data.decode('utf-8')


#
# PURPOSE:
# Send a PUT request to the server using a given key and message 
# If the server responds with a 'NO' then that means that a message with the given key already exists
# therefore, this method retries a PUT request with the key that was returned by the server 
#
# PARAMETERS:
# 'key' is a string which is the key to be sent to the server.
# 'msg' is a string to be sent to the server
#
# RETURN/SIDE EFFECTS:
# Returns the decoded response by the server
#
# NOTES:
# Opens/closes a new connection to the server
#
async def sendPutRequest(key, msg):
    og_msg = msg[KEY_LENGTH:]
    request = PUT_CMD + key.encode('utf-8') + msg.encode('utf-8') + b'\n'
    
    while True: 
        reader, writer = await asyncio.open_connection(SERVER_IP, PORT)
        writer.write(request)
        response = await reader.readline()
        writer.close()
        await writer.wait_closed()
        response = response.decode('utf-8')
        #print(f'[Response:] ', response)
    
        if response[:len(NO_RESPONSE)] == NO_RESPONSE:
            key = response[len(NO_RESPONSE):len(NO_RESPONSE) + KEY_LENGTH]
            next_key = ''.join(random.choices(string.digits, k=KEY_LENGTH))
            msg = next_key + og_msg
            request = PUT_CMD + key.encode('utf-8') + msg.encode('utf-8') + b'\n'
        else:
            return response
    
    
    
#
# PURPOSE:
# Given a key from the command line, print all associated messages in the thread
# Poll the server every 5 seconds with the latest key to retrieve the latest message
#
# PARAMETERS:
# 'key' is a string, which is a global variable
# Assume the key has been validated as an 8-digit string
#
# NOTES:
# If there is a message returned from the server, assume that meesage consists of
# of an 8-digit key and a message body
#
async def get():
    global key
    
    while True:
        get_result = await sendGetRequest()
        msg = get_result.strip()[KEY_LENGTH:]
        
        while len(msg) > 0:
            key = get_result.strip()[:KEY_LENGTH]
            print(f'Message: {msg}')
            get_result = await sendGetRequest()
            msg = get_result.strip()[KEY_LENGTH:]
        
        #print(f'Looking for key: {key}')
        await asyncio.sleep(5)



#
# PURPOSE:
# Prompt the user for a new message. This new message will be paired with a randomly generated key
# The new message and key are sent to the server by a PUT request
#
# PARAMETERS:
# 'key' is a string, which is a global variable
# Assume the key has been validated as an 8-digit string
#
# NOTES:
#
async def put():
    global key
    
    while True:
        next_key = ''.join(random.choices(string.digits, k=KEY_LENGTH))
        loop = asyncio.get_running_loop()
        try:
            print()
            new_msg = await loop.run_in_executor(None, input, f'Please enter a message for key {next_key}: ')
        except:
           break

        new_msg = next_key + new_msg
        await sendPutRequest(key, new_msg)
        

#
# PURPOSE:
# Use two co-routines to retrieve the latest message in a thread using a given key from the commandline and 
# send a new message to the server with the latest key
# The client does not quit
#
# NOTES:
# Each co-routine communicates the latest key by using the key as a global variable
#
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

