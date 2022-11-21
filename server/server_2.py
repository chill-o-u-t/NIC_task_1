import asyncio

import tcp_connection_pb2
from server.exceptions import SomeException
from utils import time_now
HOST = 'localhost'
PORT = 8000


class EchoServer(object):
    def __init__(self):
        self.message = tcp_connection_pb2.WrapperMessage()
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self.start_server())
        self.users = 0

    async def echo_handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while not reader.at_eof():
            self.users += 1
            data = await reader.read(1024)
            self.message.ParseFromString(data)
            if self.message.HasField('request_for_fast_response'):
                self.message.fast_response.current_date_time = time_now()
                writer.write(self.message.SerializeToString())
                await writer.drain()
                self.message.Clear()
            if self.message.HasField('request_for_slow_response'):
                delay = self.message.request_for_slow_response.time_in_seconds_to_sleep
                instance = tcp_connection_pb2.SlowResponse()
                instance.connected_client_count = self.users
                self.message.slow_response.CopyForm(instance)
                await asyncio.sleep(int(delay))
                writer.write(self.message.SerializeToString())
                await writer.drain()
                self.message.Clear
            else:
                raise SomeException('')
            self.users -= 1

    async def start_server(self) -> None:
        print(f'Server started on {HOST}:{PORT}')
        server = await asyncio.start_server(self.echo_handle, HOST, PORT)
        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    server = EchoServer()
    server.start_server()
