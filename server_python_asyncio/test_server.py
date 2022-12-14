import unittest

from asyncio_server import EchoServer

import tcp_connection_pb2


HOST = 'localhost'
PORT = 9999


class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        self.server = EchoServer()
        self.message = tcp_connection_pb2.WrapperMessage
        self.server.start_server()

    def test_fast_response(self):
        pass