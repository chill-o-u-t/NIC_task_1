import os
import logging

from twisted.internet import protocol, reactor
from twisted.internet.protocol import connectionDone
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.defer import Deferred

import tcp_connection_pb2
from server_python_twisted.utils import time_now


DEBUG = True

if DEBUG:
    HOST = 'localhost'
    PORT = 9999
else:
    HOST = os.getenv('SERVER_IP')
    PORT = os.getenv('DEFAULT_PORT')


def check_all():
    return all([HOST, PORT])


class TSServerProtocol(protocol.Protocol):
    """
     Server side protocol
     Each client connection corresponds to an instance.
    """

    def __init__(self, users):
        self.users = users
        self.message = tcp_connection_pb2.WrapperMessage()
        self._buffer = b""
        self.clientInfo = ""

    def connectionMade(self):
        self.clientInfo = self.transport.getPeer()
        self.users.append(self)
        logging.info(
            f'Successful connection with '
            f'{self.clientInfo.host}:{self.clientInfo.port}'
        )

    def dataReceived(self, data):
        self._buffer += data
        self.message.Clear()
        try:
            self.message.ParseFromString(self._buffer)
            logging.info('Message received successfully')
            logging.info(
                f'Message received from '
                f'{self.clientInfo.host}:{self.clientInfo.port}'
            )
            if self.message.HasField('request_for_fast_response'):
                self.fast_response()
                self._buffer = b""
                return
            if self.message.HasField('request_for_slow_response'):
                self.slow_response()
                self._buffer = b""
                return
            if len(self._buffer) >= 1024:
                logging.error(
                    f'Receive message buffer full:'
                    f'{len(self._buffer)}, {self._buffer}'
                )
                self._buffer = b""
                return
            logging.error(
                f'Only part of the message was delivered: '
                f'{self.message}, {self._buffer}'
            )
            return
        except Exception as error:
            # DATA_RECIEVED_ERROR в другом файле - константа
            # print(DATA_RECIEVED_ERROR.format(e))
            pass

    def fast_response(self):
        self.message.Clear()
        self.message.fast_response.current_date_time = time_now()
        self.send_message(self.message)

    def slow_response(self):
        client_count = len(self.users)
        delay = self.message.request_for_slow_response.time_in_seconds_to_sleep
        self.message.Clear()
        self.message.slow_response.connected_client_count = client_count
        deferred = Deferred()
        deferred.addCallback(self.send_message)
        reactor.callLater(delay, deferred.callback, self.message)

    def send_message(self, message):
        self.transport.write(message.SerializeToString())
        logging.info(f'Message successfully sent')

    def connectionLost(self, reason=connectionDone):
        logging.info('Delete user from server_python_twisted')
        self.users.remove(self)


class TSServerFactory(protocol.Factory):
    """
    Factory for instantiating the protocol on the server_python_twisted side
    """

    def __init__(self):
        self.users = []
        logging.info(f'Server started on {HOST}:{PORT}')

    def buildProtocol(self, addr):
        return TSServerProtocol(self.users)


if __name__ == '__main__':
    import configure_logging
    configure_logging()
    if not check_all():
        logging.critical('Started failed: empty host or port')
    endpoint = TCP4ServerEndpoint(reactor, PORT)
    endpoint.listen(TSServerFactory())
    reactor.run()
