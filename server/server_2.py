import asyncio
import logging

import tcp_connection_pb2
from utils import time_now
HOST = 'localhost'
PORT = 9999


class EchoServer(object):
    users_count = {}
    def __init__(self):
        self.message = tcp_connection_pb2.WrapperMessage()
        self._loop = asyncio.new_event_loop()
        self._loop.run_until_complete(self.start_server())

    async def echo_handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, users={}):
        while not reader.at_eof():
            data = await reader.read(1024)
            self.message.ParseFromString(data)
            address, port = writer.get_extra_info('peername')
            users[f'{address}:{port}'] = 1
            try:
                if self.message.HasField('request_for_fast_response'):
                    self.message.fast_response.current_date_time = time_now()
                    writer.write(self.message.SerializeToString())
                    await writer.drain()
                    self.message.Clear()
                if self.message.HasField('request_for_slow_response'):
                    delay = self.message.request_for_slow_response.time_in_seconds_to_sleep
                    instance = tcp_connection_pb2.SlowResponse()
                    instance.connected_client_count = sum(users.values())
                    msg = tcp_connection_pb2.WrapperMessage()
                    msg.slow_response.CopyFrom(instance)
                    await asyncio.sleep(int(delay))
                    writer.write(msg.SerializeToString())
                    await writer.drain()
                    self.message.Clear
                users[f'{address}:{port}'] = 0
            except Exception as error:
                print(error)

    async def start_server(self) -> None:
        server = await asyncio.start_server(
            self.echo_handle,
            HOST,
            PORT
         )
        logging.info(f'Server started on {HOST}:{PORT}')
        print(f'Server started on {HOST}:{PORT}')
        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    server = EchoServer()
    server.start_server()