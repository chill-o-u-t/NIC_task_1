import unittest
import socket
from server.tcp_connection_pb2 import *

class ServerTest(unittest.TestCase):

    def setUp(self):
        self.HOST = 'localhost'
        self.PORT = 9999
        self.message = WrapperMessage()
        self.answer = WrapperMessage()
        self.fake_client = socket.socket()
        self.fake_client.connect((self.HOST, self.PORT))

    def tearDown(self):
        self.fake_client.close()

    def test_fast_response(self):
        instance = RequestForFastResponse()
        self.message.request_for_fast_response.CopyFrom(instance)
        self.fake_client.send(self.message.SerializeToString())
        data = self.fake_client.recv(1024)
        self.answer.ParseFromString(data)
        self.assertTrue(self.answer.HasField('fast_response'))

    def test_slow_response(self):
        instance = RequestForSlowResponse()
        instance.time_in_seconds_to_sleep = 0
        self.message.request_for_slow_response.CopyFrom(instance)
        self.fake_client.send(self.message.SerializeToString())
        data = self.fake_client.recv(1024)
        self.answer.ParseFromString(data)
        self.assertTrue(self.answer.HasField('slow_response'))

"""
    def test_not_wrapper_message(self):
        instance = RequestForSlowResponse()
        instance.time_in_seconds_to_sleep = 0
        self.message.request_for_slow_response.CopyFrom(instance)
        ser = TSServerProtocol()
        with self.assertLogs() as captured:
            TSServerProtocol.dataReceived(ser, data=self.message.SerializeToString())  # Пустой WrapperMessage
        self.assertEqual(len(captured.records), 1)  # check that there is only one log message
        self.assertEqual(captured.records[0].getMessage(), "Failed sending sata: ")  # and it is the proper one
"""

if __name__ == '__main__':
    unittest.main()
