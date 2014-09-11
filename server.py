import logging
from twisted.internet import protocol, reactor, endpoints

class ResponseHandler(protocol.Protocol):
    # response types
    responses = {'ok':'1', 'error':'0'}
    apiVersion = '1.0.0'

    # formats the response message
    def sendResponse(self, message):
        # include the server api version
        response = self.apiVersion+':'+message
        self.transport.write(response)

    # handle responses
    def dataReceived(self, data):
        # receive public key. Expects key:UDID
        pieces = data.split(':')
        if len(pieces) != 2:
            self.sendResponse(self.responses['error'])
        else:
            key = pieces[0]
            uuid = pieces[1]
            print('key\n'+key+'\n\n'+uuid+'\n\n')
            # process key and UUID
            self.sendResponse(self.responses['ok'])

class ResponseFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ResponseHandler()

endpoints.serverFromString(reactor, "tcp:1234").listen(ResponseFactory())
reactor.run()