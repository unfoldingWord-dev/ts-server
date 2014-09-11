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
    device_key_path = str(data['key_path']['user'])
    port = str(data['port'])

    # validate configuration values
    if user_key_path == "" or device_key_path == "" or port == "":
        print("invalid configuration values")
        exit()

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

    # handle responses
    def dataReceived(self, json_data):
        # expects {'key':'public key', 'udid':'device id', 'username':'an optional username'}
        try:
            data = json.loads(json_data)
        except ValueError:
            print "Unexpected error:", sys.exc_info()[0]
            self.sendError('invalid request')
            return

        if 'key' not in data or data['key'] == "" or 'udid' not in data or data['udid'] == "":
            self.sendError('incomplete request')
        else:
            print('key\n'+data['key']+'\n\nudid\n'+data['udid']+'\n\n')
            # TODO: process key and UUID
            self.sendOk('done')

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