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
        self.tcp_socket = QTcpSocket(self)
        self.tcp_socket.readyRead.connect(self.deal_communication)

    @staticmethod
    def is_empty(data):
        """
        Проверка объекта на наличие данных,
        если объект пуст или равен 0 возвращает False.
        :param data:
        :return:
        """
        return data == 0 or data == ''

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


class UiMainWindow(Client):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(800, 600)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central-widget")

        # text_edits
        self.text_edit_host = QtWidgets.QTextEdit(self.central_widget)
        self.text_edit_host.setGeometry(QtCore.QRect(210, 50, 104, 40))
        self.text_edit_host.setObjectName("textEdit")
        self.text_edit_port = QtWidgets.QTextEdit(self.central_widget)
        self.text_edit_port.setGeometry(QtCore.QRect(370, 50, 104, 40))
        self.text_edit_port.setObjectName("textEdit_2")
        self.text_edit_timeout = QtWidgets.QTextEdit(self.central_widget)
        self.text_edit_timeout.setGeometry(QtCore.QRect(40, 130, 104, 40))
        self.text_edit_timeout.setObjectName("textEdit_3")
        self.text_edit_delay = QtWidgets.QTextEdit(self.central_widget)
        self.text_edit_delay.setGeometry(QtCore.QRect(210, 290, 104, 40))
        self.text_edit_delay.setObjectName("textEdit_4")

        # labels
        self.label_ip = QtWidgets.QLabel(self.central_widget)
        self.label_ip.setGeometry(QtCore.QRect(210, 30, 100, 13))
        self.label_ip.setObjectName("label")
        self.label_port = QtWidgets.QLabel(self.central_widget)
        self.label_port.setGeometry(QtCore.QRect(370, 30, 100, 13))
        self.label_port.setObjectName("label_2")
        self.label_connected_status = QtWidgets.QLabel(self.central_widget)
        self.label_connected_status.setGeometry(
            QtCore.QRect(520, 50, 170, 40)
        )
        self.label_connected_status.setObjectName("label_3")
        self.label_timeout = QtWidgets.QLabel(self.central_widget)
        self.label_timeout.setGeometry(QtCore.QRect(40, 110, 100, 13))
        self.label_timeout.setObjectName("label_4")
        self.label_default_timeout = QtWidgets.QLabel(self.central_widget)
        self.label_default_timeout.setGeometry(QtCore.QRect(40, 170, 100, 13))
        self.label_default_timeout.setObjectName("label_5")
        self.label_delay = QtWidgets.QLabel(self.central_widget)
        self.label_delay.setGeometry(QtCore.QRect(210, 270, 100, 13))
        self.label_delay.setObjectName("label_6")
        self.label_output_fast = QtWidgets.QLabel(self.central_widget)
        self.label_output_fast.setGeometry(QtCore.QRect(380, 290, 310, 40))
        self.label_output_fast.setObjectName("label_7")
        self.label_output_slow = QtWidgets.QLabel(self.central_widget)
        self.label_output_slow.setGeometry(QtCore.QRect(380, 210, 310, 40))
        self.label_output_slow.setObjectName("label_8")

        # buttons
        self.pushButton_2 = QtWidgets.QPushButton(self.central_widget)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 210, 111, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.central_widget)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 290, 111, 41))
        self.pushButton_3.setObjectName("pushButton_3")

        # logger
        self.logger_console = QtWidgets.QTextEdit(self.central_widget)
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

        # other
        main_window.setCentralWidget(self.central_widget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        logging.info('Interface created')

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_ip.setText(_translate("MainWindow", "IP address"))
        self.label_port.setText(_translate("MainWindow", "Port"))
        self.label_connected_status.setText(
            _translate("MainWindow", "Successfully connection or error")
        )
        self.pushButton_2.setText(_translate("MainWindow", "Fast Request"))
        self.pushButton_3.setText(_translate("MainWindow", "Slow Request"))
        self.label_timeout.setText(_translate("MainWindow", "TimeOut"))
        self.label_default_timeout.setText(
            _translate("MainWindow", "Default TimeOut: 1")
        )
        self.label_delay.setText(_translate("MainWindow", "Delay"))
        self.label_output_fast.setText(
            _translate("MainWindow", "output here")
        )
        self.label_output_slow.setText(
            _translate("MainWindow", "output here")
        )
        self.pushButton_3.clicked.connect(self.slow_request)
        self.pushButton_2.clicked.connect(self.fast_request)

    def check_data_host_and_port(self):
        """
        Проверяет корректность введеных Ip и Port.
        :return:
        """
        host = self.text_edit_host.toPlainText()
        text_port = self.text_edit_port.toPlainText()
        if self.is_empty(host):
            self.label_connected_status.setText('Host is none')
            logging.error('Host is empty')
            return
        if self.is_empty(text_port):
            self.label_connected_status.setText('Port is None')
            logging.error('Port is empty')
            return
        if not self.check_ip(host):
            self.label_connected_status.setText('Invalid IP')
            logging.error(f'Introduced ip is wrong: {host}')
            return
        if len(text_port) > 4:
            self.label_connected_status.setText('Invalid Port')
            logging.error(
                f'Len of port ({len(text_port)}) more then max port len'
            )
            return
        try:
            port = int(text_port)
        except ValueError:
            self.label_connected_status.setText('Port error')
            logging.error('Can`t convert string port to int')
            return
        self.make_request(host, port)
        #       self.check_timeout()

    def check_timeout(self):
        timeout = self.text_edit_timeout.toPlainText()
        try:
            timeout_digit = int(timeout)
        except ValueError:
            logging.info('Timeout is empty or wrong')
            return
        if timeout_digit in TIMEOUT:
            self.time_out = int(self.text_edit_timeout.toPlainText())
            return
        logging.info('Timeout is empty, default is 1')
        return

    def check_delay(self):
        delay_text = self.text_edit_delay.toPlainText()
        if self.is_empty(delay_text):
            delay = 10
        else:
            delay = int(delay_text)
        if delay < 10 or delay > 1000:
            logging.error('Can`t set delay more 1000 or less 10')
            return 1
        logging.info(f'Delay set at {delay // 10} sec.')
        return delay // 10

    def slow_request(self):
        if not self.check_data_host_and_port():
            return
        instance = tcp_connection_pb2.RequestForSlowResponse()
        try:
            instance.time_in_seconds_to_sleep = self.check_delay()
            self.message.request_for_slow_response.CopyFrom(instance)
            self.tcp_socket.write(self.message.SerializeToString())
            self.message.Clear()
            logging.info('Slow request message is sending now')
        except Exception as error:
            logging.error(f'Data sending failed: {error}')
            print(error)

    def fast_request(self) -> None:
        if not self.check_data_host_and_port():
            return
        instance = tcp_connection_pb2.RequestForFastResponse()
        try:
            self.message.request_for_fast_response.CopyFrom(instance)
            self.tcp_socket.write(self.message.SerializeToString())
            logging.info('Fast request message is sending now')
            self.message.Clear()
        except Exception as error:
            logging.error(f'Data sending failed: {error}')

    def make_request(self, host, port) -> None:
        try:
            self.tcp_socket.connectToHost(host, port, QIODevice.ReadWrite)
            logging.info(f'Successful connection: {host}:{port}')
        except Exception as error:
            logging.error(f'Connection failed: {error}')

    def deal_communication(self) -> None:
        instr = QDataStream(self.tcp_socket)
        instr.setVersion(QDataStream.Qt_5_0)
        if self.blockSize == 0:
            if self.tcp_socket.bytesAvailable() < 2:
                return
            self.blockSize = instr.readUInt16()
        if self.tcp_socket.bytesAvailable() < self.blockSize:
            return
        self.message.ParseFromString(instr.readQString())
        if self.message.HasField('request_for_fast_response'):
            self.label_output_fast.setText(
                self.message.fast_response.current_date_time
            )
        elif self.message.HasField('request_for_slow_response'):
            self.label_output_slow.setText(
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
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    logging.info('Started client')

    sys.exit(app.exec())
