import unittest

from .asyncio_server import EchoServer
import tcp_connection_pb2


class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        self.server = EchoServer()
        self.message = tcp_connection_pb2.WrapperMessage

