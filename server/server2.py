from twisted.internet import protocol, reactor
from twisted.internet.protocol import connectionDone
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.defer import Deferred
# TCP4ServerEndpoint требуется win32api
from datetime import datetime
import tcp_connection_pb2

message = tcp_connection_pb2.WrapperMessage()


# 2, определить класс протокола на стороне сервера
class TSServerProtocol(protocol.Protocol):
    """
     Протокол на стороне сервера
     Каждое клиентское соединение соответствует экземпляру.
    """

    def __init__(self, users):
        self.users = users
        self.clientInfo = ""  # clientInfo сохранит информацию о клиентском соединении.

    def connectionMade(self):
        # TODO: логи в файл
        self.clientInfo = self.transport.getPeer()
        self.users.append(self)
        print("Соединение с% s" % (self.clientInfo))

    def dataReceived(self, data):
        message.ParseFromString(data)
        print(message)

        if message.HasField('request_for_fast_response'):
            self.fast_response()
            # отвечать на  RequestForFastResponse сообщением  FastResponse
            # с текущем временем на машине сервера
        elif message.HasField('request_for_slow_response'):
            self.slow_response(message)
        else:
            # тут будет ошибка
            print("что-то плохо мне")
        message.Clear()

    def slow_response(self, data):
        client_count = len(self.users)
        delay = data.request_for_slow_response.time_in_seconds_to_sleep
        instance = tcp_connection_pb2.SlowResponse()
        instance.connected_client_count = client_count

        msg = tcp_connection_pb2.WrapperMessage()
        msg.slow_response.CopyFrom(instance)
        # sleep
        deferred = Deferred()
        deferred.addCallback(self.send_message)
        reactor.callLater(delay, deferred.callback, msg)

    def fast_response(self):
        time_now = datetime.now().strftime("%Y%m%dT%H%M%S.%f")
        message.fast_response.current_date_time = time_now
        self.send_message(message)
        message.Clear()

    def send_message(self, msg):
        self.transport.write(msg.SerializeToString())  # utf-8??

    def connectionLost(self, reason=connectionDone):
        # TODO: логи
        print('Delete user from server')
        self.users.remove(self)


# 3. Определите класс фабрики на стороне сервера
class TSServerFactory(protocol.Factory):
    def __init__(self):
        self.users = []

    def buildProtocol(self, addr):
        return TSServerProtocol(self.users)


# 4, используйте реактор для запуска мониторинга порта
if __name__ == '__main__':
    PORT = 8000  # TODO: читываем из файла
    endpoint = TCP4ServerEndpoint(reactor, PORT)
    endpoint.listen(TSServerFactory())
    reactor.run()
