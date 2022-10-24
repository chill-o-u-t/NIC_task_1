from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog
from PyQt5.QtNetwork import *

import utils


class Server(QDialog):
    def __init__(self):
        super().__init__()
        self.tcpServer = None

    def session_opened(self):
        self.tcpServer = QTcpServer(self)
        address = QHostAddress(utils.IP)
        if not self.tcpServer.listen(address, utils.IP):
            self.close()
            return
        self.tcpServer.newConnection.connect(self.dealCommunication)

    def deal_communication(self):
        clientConnection = self.tcpServer.nextPendingConnection()
        block = QByteArray()
        out = QDataStream(block, QIODevice.ReadWrite)
        out.setVersion(QDataStream.Qt_5_0)
        out.writeUInt16(0)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)
        clientConnection.waitForReadyRead()
        instr = clientConnection.readAll()
        clientConnection.disconnected.connect(clientConnection.deleteLater)
        clientConnection.write(block)
        clientConnection.disconnectFromHost()


