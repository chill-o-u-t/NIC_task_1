import logging

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtNetwork import *

import utils
from logger_config import logger_conf


class ClientWindow(QDialog):
    def __init__(self, wait_to_connection):
        super().__init__()
        self.tcpSocket = QTcpSocket(self)
        self.blockSize = 0
        self.make_request()
        self.tcpSocket.waitForConnected(wait_to_connection)
        self.tcpSocket.readyRead.connect(self.deal_communication)
        self.tcpSocket.readyRead.connect(self.dealCommunication)
        self.tcpSocket.error.connect(self.displayError)

    def make_request(self):
        self.tcpSocket.connectToHost(utils.IP, utils.PORT, QIODevice.ReadWrite)

    def deal_communication(self):
        socket = QDataStream(self.tcpSocket)
        socket.setVersion(QDataStream.Qt_5_0)
        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return
            self.blockSize = socket.readUInt16()
        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return
        data = str(socket.readString())
        # Где-то тут будет перевод из QByteArray в строку
        if len(data) > 3: #Нужна другая реализация, чтобы отличать запросы
            ui.label_2.SetText(data)
        else:
            ui.label_3.SetText(data)
        # Как подключить класс Клиента для соеденения к классу интерфейса, хотя скорее все в 1 класс

    def request_for_fast_response(self):
        pass

    def request_for_slow_response(self, delay):
        pass


if __name__ == '__main__':
    import sys
    logger_conf()
    logging.info('Приложение запущено')
    app = QApplication(sys.argv)
    client = ClientWindow()
    # ----
    client.request_for_fast_response()
    delay = ''
    client.request_for_slow_response(delay=delay)
    # ----
    sys.exit(client.exec_())
