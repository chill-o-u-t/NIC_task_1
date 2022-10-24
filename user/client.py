from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtNetwork import *

import utils


class ClientWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.tcpSocket = QTcpSocket(self)
        self.blockSize = 0
        self.make_request()
        self.tcpSocket.waitForConnected()
        self.tcpSocket.readyRead.connect(self.deal_communication)

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


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    client = ClientWindow()
    sys.exit(client.exec_())
