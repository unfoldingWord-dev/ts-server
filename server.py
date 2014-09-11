import logging
from twisted.internet import protocol, reactor, endpoints

class ResponseHandler(protocol.Protocol):
    # response types
    responses = {'ok':'1', 'error':'0'}

    # handle responses
    def dataReceived(self, data):
        # receive public key
        print(data)
        self.transport.write(self.responses['ok'])

class ResponseFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ResponseHandler()

endpoints.serverFromString(reactor, "tcp:1234").listen(ResponseFactory())
reactor.run()