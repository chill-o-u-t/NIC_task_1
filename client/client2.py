from twisted.internet import protocol, reactor
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ReconnectingClientFactory as ClFactory
from twisted.internet.defer import Deferred

import tcp_connection_pb2

message = tcp_connection_pb2.WrapperMessage()


# 2, определить класс протокола клиента
class TSClientProtocol(Protocol):
    def sendData(self):
        data = input("> ")  # TODO: кнопка в интерфейсе qt вместо input()
        delay = 1  # TODO: данные из файла достать
        if data == 'Slow':
            instance = tcp_connection_pb2.RequestForSlowResponse()
            if delay:
                instance.time_in_seconds_to_sleep = delay
            message.request_for_slow_response.CopyFrom(instance)
        elif data == 'exit':
            command = 'exit'

        else:
            instance = tcp_connection_pb2.RequestForFastResponse()
            message.request_for_fast_response.CopyFrom(instance)
        self.transport.write(message.SerializeToString())
        message.Clear()

    def connectionMade(self):
        print("Connection successful from client")
        self.sendData()

    def dataReceived(self, data):
        message.ParseFromString(data)
        print("Данные получены с сервера:% s" % (message))
        if message.HasField('request_for_fast_response'):
            print('Current time on the server:', message.fast_response.current_date_time)
        elif message.HasField('request_for_slow_response'):
            print('Number of connected clients:', message.slow_response.connected_client_count)

        message.Clear()
        self.sendData()


# 3, определить класс фабрики клиента
class TSClientFactory(ClFactory):
    protocol = TSClientProtocol

    def clientConnectionFailed(self, connector, reason):  # вообще не можем подключиться
        # TODO: логи в файл, переподключение c delay
        delay = 5
        print('connection failed:', reason)
        # переподключение
        # ClFactory.clientConnectionFailed(self, connector, reason)
        deferred = Deferred()
        deferred.addCallback(ClFactory.clientConnectionFailed)
        reactor.callLater(delay, deferred.callback, self, connector, reason)

    def clientConnectionLost(self, connector, reason):  # были подключены
        # TODO: логи в файл
        print('connection lost:', reason)
        # переподключение
        # TODO: переподключение c delay
        delay = 5
        deferred = Deferred()
        deferred.addCallback(ClFactory.clientConnectionLost)
        reactor.callLater(delay, deferred.callback, self, connector, reason)
        # ClFactory.clientConnectionLost(self, connector, reason)


# 4, используйте реактор, чтобы начать соединение
if __name__ == '__main__':
    HOST = 'localhost'  # TODO: считываем из файла
    PORT = 8000  # TODO: считываем из файла
    reactor.connectTCP(HOST, PORT, TSClientFactory())
    reactor.run()
