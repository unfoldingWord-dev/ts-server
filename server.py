import logging
from twisted.internet import protocol, reactor, endpoints
import json

# load settings from the config file
json_data = open('config.json')
data = json.load(json_data)
json_data.close()

user_key_path = data['key_path']['user']
device_key_path = data['key_path']['user']

class ResponseHandler(protocol.Protocol):
    global user_key_path, device_key_path
    apiVersion = '1.0.0'

    # sends an error message to the client
    def sendError(self, message):
        response = '{"version":"'+self.apiVersion+'","error":"'+message+'"}'
        self.transport.write(response)

    # sends a ok message to the client
    def sendOk(self, message):
        response = '{"version":"'+self.apiVersion+'","ok":"'+message+'"}'
        self.transport.write(response)

    # handle responses
    def dataReceived(self, json_data):
        # expects {'key':'public key', 'udid':'device id', 'username':'an optional username'}
        try:
            data = json.loads(json_data)
        except ValueError:
            self.sendError('invalid request')
            return

        if data['key'] is None or data['udid'] is None:
            self.sendError('incomplete request')
        else:
            print('key\n'+data['key']+'\n\n'+data['udid']+'\n\n')
            # process key and UUID
            self.sendOk('done')

class ResponseFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ResponseHandler()

endpoints.serverFromString(reactor, "tcp:1234").listen(ResponseFactory())
reactor.run()