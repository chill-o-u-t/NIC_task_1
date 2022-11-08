# 1, библиотека, на которую нужно ссылаться
from twisted.internet import protocol, reactor
from twisted.internet.protocol import connectionDone
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet.defer import Deferred
# TCP4ServerEndpoint требуется win32api
from datetime import datetime


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
        recData = data.decode('utf-8')
        # print("Получены данные от % s: % s" % (self.clientInfo, recData))
        print(recData)
        if recData == 'amount':  # условное обозначение
            data = str(len(self.users))
            self.send_message(data)
            #self.transport.write(str(len(self.users)).encode('utf-8'))
        elif recData == 'exit':
            reason = 'Пользователь вышел'
            self.connectionLost(self, reason)
        else:  # блок try except временно
            try:
                data, delay = recData.split()
                time = datetime.now().strftime("%Y%m%dT%H%M%S.%f")
                deferred = Deferred()
                deferred.addCallback(self.send_message)
                reactor.callLater(int(delay), deferred.callback, time)
            except:
                self.send_message('что-то не так(передай данные нормально)')
                # self.send_message(time)
            # self.transport.write(time.encode('utf-8'))

    def send_message(self, msg):
        self.transport.write(msg.encode('utf-8'))

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
