import asyncio
from collections import defaultdict

import tcp_connection_pb2
from utils import time_now
HOST = 'localhost'
PORT = 8000


class EchoServer(object):
    def __init__(self):
        self.message = tcp_connection_pb2.WrapperMessage()
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self.start_server())
        self.reader = asyncio.StreamReader
        self.writer = asyncio.StreamWriter
        self.users = defaultdict()

    def connections(self):
        pass

    async def echo_handle(self):
        protocol = tcp_connection_pb2.WrapperMessage
        while not self.reader.at_eof():
            data = await self.reader.read(1024)
            message = protocol.SerializeToString(data)
            assert type(message) == str
            address, port = self.writer.get_extra_info('peername')
            self.users[f'{address}:{port}'] = 1
            if message == '0':
                msg = protocol.fast_response.ParseToString(time_now())
            if 1000 > int(message) > 10:
                msg = protocol.slow_response.ParseToString(sum(self.users.values()))
                await asyncio.sleep(int(message))
            self.writer.write(msg)
            await self.writer.drain()
            self.users[f'{address}:{port}'] = 0

    async def start_server(self) -> None:
        server = await asyncio.start_server(self.echo_handle, HOST, PORT)
        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    server = EchoServer()
