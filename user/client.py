import logging
import re
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import QDataStream, QIODevice
from PyQt6.QtNetwork import QTcpSocket
from PyQt6.QtWidgets import QDialog

import tcp_connection_pb2
from user.constants import TIMEOUT
from logger_config import CustomLogFormatter


class Client(QDialog):
    def __init__(self):
        super().__init__()
        self.blockSize = 0
        self.message = tcp_connection_pb2.WrapperMessage()
        self.time_out = 1000
        self.tcpSocket = QTcpSocket(self)
        self.tcpSocket.readyRead.connect(self.deal_communication)

    @staticmethod
    def is_empty(object):
        """
        Проверка объекта на наличие данных,
        если объект пуст или равен 0 возвращает False.
        :param object:
        :return:
        """
        return object == 0 or object == ''

    @staticmethod
    def check_ip(ip):
        """
        Проверка введенного ip адреса на соответствие формату.
        :param ip:
        :return:
        """
        if re.match(
            '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip
        ) is None:
            return False
        for block in map(int,  ip.split('.')):
            if block > 255:
                return False
        return True


class Ui_MainWindow(Client):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #text_edits
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(210, 50, 104, 40))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(370, 50, 104, 40))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(40, 130, 104, 40))
        self.textEdit_3.setObjectName("textEdit_3")
        self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(210, 290, 104, 40))
        self.textEdit_4.setObjectName("textEdit_4")

        #labels
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 30, 100, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(370, 30, 100, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(520, 50, 170, 40))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 110, 100, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 170, 100, 13))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(210, 270, 100, 13))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(380, 290, 310, 40))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(380, 210, 310, 40))
        self.label_8.setObjectName("label_8")

        #buttons
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 210, 111, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 290, 111, 41))
        self.pushButton_3.setObjectName("pushButton_3")

        #logger
        self.logger_console = QtWidgets.QTextEdit(self.centralwidget)
        self.logger_console.setGeometry(QtCore.QRect(40, 361, 641, 211))
        self.logger_console.setObjectName("textBrowser")
        self.logger_console.setStyleSheet(
            """
            QTextEdit {
                background-color: #000;
                color: #00ff00
            }"""
        )
        sys.stdout.write = self.request_std(sys.stdout.write)
        sys.stderr.write = self.request_std(sys.stderr.write)

        #other
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "IP address"))
        self.label_2.setText(_translate("MainWindow", "Port"))
        self.label_3.setText(
            _translate("MainWindow", "Succesfull conection or error")
        )
        self.pushButton_2.setText(_translate("MainWindow", "Fast Request"))
        self.pushButton_3.setText(_translate("MainWindow", "Slow Request"))
        self.label_4.setText(_translate("MainWindow", "TimeOut"))
        self.label_5.setText(_translate("MainWindow", "Default TimeOut: 1"))
        self.label_6.setText(_translate("MainWindow", "Delay"))
        self.label_7.setText(_translate("MainWindow", "output here"))
        self.label_8.setText(_translate("MainWindow", "output here"))
        self.pushButton_3.clicked.connect(self.slow_request)
        self.pushButton_2.clicked.connect(self.fast_request)

    def check_data_host_and_port(self):
        """
        Проверяет корректность введеных Ip и Port.
        :return:
        """
        host = self.textEdit.toPlainText()
        text_port = self.textEdit_2.toPlainText()
        if self.is_empty(host):
            self.label_3.setText('Host is none')
            return
        if self.is_empty(text_port):
            self.label_3.setText('Port is None')
            return
        if not self.check_ip(host):
            self.label_3.setText('Invalid IP')
            return
        if len(text_port) > 4:
            self.label_3.setText('Invalid Port')
            return
        try:
            port = int(text_port)
        except ValueError:
            self.label_3.setText('Port error')
            return
        self.make_request(host, port)
        #       self.check_timeout()

    def check_timeout(self):
        timeout = self.textEdit_3.toPlainText()
        try:
            timeout_digit = int(timeout)
        except ValueError:
            logging.info('Timeout is empty or wrong')
        if timeout_digit in TIMEOUT:
            self.time_out = int(self.textEdit_3.toPlainText())
            return
        logging.info('Timeout is empty, default is 1')
        return

    def check_delay(self):
        delay_text = self.textEdit_4.toPlainText()
        if self.is_empty(delay_text):
            delay = 10
        else:
            delay = int(delay_text)
        if delay < 10 or delay > 1000:
            logging.error('Задержка не может превыщать 1000 мс или быть меньшше 10 мс')
            return 1
        return delay // 10

    def slow_request(self):
        if not self.check_data_host_and_port():
            print('error') # vremenno
            return
        instance = tcp_connection_pb2.RequestForSlowResponse()
        try:
            instance.time_in_seconds_to_sleep = self.check_delay()
            self.message.request_for_slow_response.CopyFrom(instance)
            self.tcpSocket.write(self.message.SerializeToString())
            print(self.message)
            self.message.Clear()
            logging.info('Successfully sending data')
        except Exception as error:
            logging.error(f'Data sending failed: {error}')
            print(error)

    def fast_request(self) -> None:
        logging.info('fast request')
        self.logger_console.insertPlainText(
            '!'
        )
        if not self.check_data_host_and_port():
            return
        instance = tcp_connection_pb2.RequestForFastResponse()
        try:
            self.message.request_for_fast_response.CopyFrom(instance)
            self.tcpSocket.write(self.message.SerializeToString())
            self.message.Clear()
        except Exception as error:
            return

    def make_request(self, host, port) -> None:
        try:
            self.tcpSocket.connectToHost(host, port, QIODevice.ReadWrite)
            logging.info(f'Successful connection: {host}:{port}')
        except Exception as error:
            logging.error(f'Connection failed: {error}')

    def deal_communication(self) -> None:
        instr = QDataStream(self.tcpSocket)
        instr.setVersion(QDataStream.Qt_5_0)
        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return
            self.blockSize = instr.readUInt16()
        if self.tcpSocket.bytesAvailable() < self.blockSize:
            return
        self.message.ParseFromString(instr.readQString())
        if self.message.HasField('request_for_fast_response'):
            self.label_7.setText(
                self.message.fast_response.current_date_time
            )
        elif self.message.HasField('request_for_slow_response'):
            self.label_8.setText(
                self.message.slow_response.connected_client_count
            )
            logging.info('Successful data received')
        else:
            logging.error('')
            self.message.Clear()
            return
        self.message.Clear()

    def request_std(self, func):
        def inner(inputStr):
            cursor = QTextCursor(self.logger_console.document())
            cursor.setPosition(0)
            self.logger_console.setTextCursor(cursor)
            self.logger_console.insertPlainText(inputStr)
            return func(inputStr)
        return inner


if __name__ == "__main__":
    import sys
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomLogFormatter())
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger = logging.getLogger("* TCP_client *")

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    logging.info('Started client')

    sys.exit(app.exec())
