#!/usr/bin/env python

import logging
import sys
from twisted.internet import protocol, reactor, endpoints
import json
import os.path

# global variables
api_version = "1.0.0"
user_key_path = ""
device_key_path = ""
port = ""

# reads in the config file
def loadConfig(config_path):
    global user_key_path, device_key_path, port

    if not os.path.isfile(config_path):
        print("the configuration file is missing")
        exit()

    # load settings from the config file
    json_data = open(config_path)
    try:
        data = json.load(json_data)
    except ValueError:
        print("the configuration file could not be parsed")
        exit()
    json_data.close()

    # validate configuration
    if 'port' not in data or 'key_path' not in data or 'user' not in data['key_path'] or 'device' not in data['key_path']:
        print("missing some configuration details")
        exit()

    user_key_path = str(data['key_path']['user'])
    device_key_path = str(data['key_path']['device'])
    port = str(data['port'])

    # validate configuration values
    if user_key_path == "" or device_key_path == "" or port == "":
        print("invalid configuration values")
        exit()

    # make sure directories exist
    if not os.path.isdir(user_key_path):
        print('--------------------------------------------------------------')
        print('Configuration warning:')
        print('could not locate the user key path please make sure it exists')
        print('path: '+user_key_path)
        print('--------------------------------------------------------------\n')
    if not os.path.isdir(device_key_path):
        print('--------------------------------------------------------------')
        print('Configuration warning:')
        print('could not locate the device key path please make sure it exists')
        print(device_key_path)
        print('--------------------------------------------------------------')

class ResponseHandler(protocol.Protocol):
    global user_key_path, device_key_path, api_version

    # sends an error message to the client
    def sendError(self, message):
        response = '{"version":"'+api_version+'","error":"'+message+'"}'
        self.transport.write(response)

    # sends a ok message to the client
    def sendOk(self, message):
        response = '{"version":"'+api_version+'","ok":"'+message+'"}'
        self.transport.write(response)

    # saves the data sent by the client
    def processData(self, data):
        if 'username' in data:
            key_path = user_key_path+'/'+data['username']+'.pub'
            if os.path.isfile(key_path):
                with open(key_path) as old_file:
                    if old_file.read() == data['key']:
                        # same key
                        self.sendOk("done")
                        return
                    else:
                        # username already taken
                        self.sendError("duplicate username")
                        return
        else:
            key_path = device_key_path+'/'+data['udid']+'.pub'
            # NOTE: device id's will always replace the old key

        f = open(key_path, 'w')
        f.write(data['key'])
        f.close()
        self.sendOk("done")

    # handle responses
    def dataReceived(self, json_data):
        # expects {'key':'public key', 'udid':'device id', 'username':'an optional username'}
        try:
            data = json.loads(json_data)
        except ValueError:
            print("Unexpected error:", sys.exc_info()[0])
            self.sendError('invalid request')
            return

        if 'key' not in data or data['key'] == "" or 'udid' not in data or data['udid'] == "":
            self.sendError('incomplete request')
        else:
            self.processData(data)

class ResponseFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ResponseHandler()

loadConfig("config.json")

print('--------------------------')
print('Translation Studio Server')
print('Version: '+api_version)
print('Listening on port: '+port)
print('--------------------------\n')

endpoints.serverFromString(reactor, 'tcp:'+port).listen(ResponseFactory())
reactor.run()
