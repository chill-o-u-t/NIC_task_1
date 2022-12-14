import unittest
import sys

from PyQt6 import QtCore, QtWidgets

import tcp_connection_pb2
from .client import UiMainWindow, MainWindow, Client


class TestClient(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_host(self):
        self.assertTrue(Client.check_ip('localhost'))
