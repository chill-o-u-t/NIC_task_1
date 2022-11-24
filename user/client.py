import logging
import re

from PyQt5 import QtCore, QtWidgets

import tcp_connection_pb2
from user.constants import TIMEOUT

TEXT = "MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#00aa00;\">logs </span></p></body></html>"


from PyQt5.QtCore import QDataStream, QIODevice
from PyQt5.QtWidgets import QDialog
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket


class Client(QDialog):
    def __init__(self):
        super().__init__()
        self.blockSize = 0
        self.message = tcp_connection_pb2.WrapperMessage()
        self.time_out = 1000
        self.tcpSocket = QTcpSocket(self)
        self.tcpSocket.readyRead.connect(self.deal_communication)


class Ui_MainWindow(Client):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(210, 50, 104, 40))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(370, 50, 104, 40))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 30, 100, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(370, 30, 100, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(520, 50, 170, 40))
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 210, 111, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 290, 111, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.textEdit_3 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_3.setGeometry(QtCore.QRect(40, 130, 104, 40))
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 110, 100, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 170, 100, 13))
        self.label_5.setObjectName("label_5")
        self.textEdit_4 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_4.setGeometry(QtCore.QRect(210, 290, 104, 40))
        self.textEdit_4.setObjectName("textEdit_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(210, 270, 100, 13))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(380, 290, 310, 40))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(380, 210, 310, 40))
        self.label_8.setObjectName("label_8")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(40, 361, 641, 211))
        self.textBrowser.setObjectName("textBrowser")
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
        self.label_3.setText(_translate("MainWindow", "Succesfull conection or error"))
        self.pushButton_2.setText(_translate("MainWindow", "Fast Request"))
        self.pushButton_3.setText(_translate("MainWindow", "Slow Request"))
        self.label_4.setText(_translate("MainWindow", "TimeOut"))
        self.label_5.setText(_translate("MainWindow", "Default TimeOut: 1"))
        self.label_6.setText(_translate("MainWindow", "Delay"))
        self.label_7.setText(_translate("MainWindow", "output slow /////////////////////////////////////////////////////////////"))
        self.label_8.setText(_translate("MainWindow", "output fast /////////////////////////////////////////////////////////////"))
        #self.textBrowser.setHtml(_translate(TEXT))
        self.pushButton_3.clicked.connect(self.slow_request)
        self.pushButton_2.clicked.connect(self.fast_request)

    def check_data_host_and_port(self):
        text_host = self.textEdit.toPlainText()
        text_port = self.textEdit_2.toPlainText()
        if text_host == '':
            self.label_3.setText('Host is none')
            return
        if text_port == '':
            self.label_3.setText('Port is None')
            return
        if re.match(
            '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text_host
        ) is None:
            self.label_3.setText('Invalid IP')
            return
        for block in map(int,  text_host.split('.')):
            if block > 255:
                self.label_3.setText('Invalid IP')
                return
        if len(text_port) > 4:
            self.label_3.setText('Port error')
            return
        try:
            port = int(text_port)
        except ValueError:
            self.label_3.setText('Port error')
            return
        try:
            if int(self.textEdit_3.toPlainText()) in TIMEOUT:
                self.time_out = int(self.textEdit_3.toPlainText())
        except Exception:
            logging.info('Set default timeout 1 second')
        self.make_request('localhost', port)
        self.label_3.setText('Successful connection')
        return True

    def check_delay(self):
        delay_text = self.textEdit_4.toPlainText()
        if delay_text == '':
            delay = 10
        else:
            delay = int(delay_text)
        if delay < 10 or delay > 1000:
            # logging
            return
        return delay // 10

    def slow_request(self):
        if not self.check_data_host_and_port():
            print('error')
            return
        instance = tcp_connection_pb2.RequestForSlowResponse()
        try:
            instance.time_in_seconds_to_sleep = self.check_delay()
            self.message.request_for_slow_response.CopyFrom(instance)
            self.tcpSocket.write(self.message.SerializeToString())
            print(self.message)
            self.message.Clear()
        except Exception as error:
            print(error)

    def fast_request(self) -> None:
        if not self.check_data_host_and_port():
            print('error')
        instance = tcp_connection_pb2.RequestForFastResponse()
        try:
            self.message.request_for_fast_response.CopyFrom(instance)
            self.tcpSocket.write(self.message.SerializeToString())
            print(self.message)
            self.message.Clear()
        except Exception as error:
            print(error)

    def make_request(self, host, port) -> None:
        print(f'{host}:{port}')
        self.tcpSocket.connectToHost(host, port, QIODevice.ReadWrite)

    def deal_communication(self) -> None:
        instr = QDataStream(self.tcpSocket)
        instr.setVersion(QDataStream.Qt_5_0)
        if self.blockSize == 0:
            if self.tcpSocket.bytesAvailable() < 2:
                return
            self.blockSize = instr.readUInt16()
        if self.tcpSocket.bytesAvailable() < self.blockSize:
            #print(1)
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

    def create_logger(path, widget: QtWidgets.QTextEdit) -> None:
        log = logging.getLogger('main')
        log.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            ('#%(levelname)-s, %(pathname)s, line %(lineno)d, [%(asctime)s]: '
             '%(message)s'), datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            (
                '#%(levelname)-s, %(pathname)s, '
                'line %(lineno)d: %(message)s'
            )
        )
        log_window_formatter = logging.Formatter(
            '#%(levelname)-s, %(message)s\n'
        )
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)

        log_window_handler = logging.Handler()
        log_window_handler.emit = lambda record: widget.insertPlainText(
            log_window_handler.format(record)
        )
        log_window_handler.setLevel(logging.DEBUG)
        log_window_handler.setFormatter(log_window_formatter)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
