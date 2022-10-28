import asyncio

from utils import time_now


class EchoServer(object):

    def __init__(self, host, port, loop=None):
        self._loop = loop or asyncio.get_event_loop()
        self._server = asyncio.start_server(
            self.handle_connection,
            host=host,
            port=port,
            #loop=self._loop
        )

    def start_server(self, and_loop=True):
        self._server = self._loop.run_until_complete(self._server)
        if and_loop:
            self._loop.run_forever()

    def close_server(self, and_loop=True):
        self._server.close()
        if and_loop:
            self._loop.close()

    def count_of_connections(self):
        r = 0
        return str(r)

    @asyncio.coroutine
    def handle_connection(self, reader, writer):
        while not reader.at_eof():
            try:
                # tod: Не понятно, что делать с получением таймаута
                data = yield from asyncio.wait_for(reader.readline(), timeout=None)
                writer.write(data)
                if data is None:
                    writer.write(time_now)
                if data is not None:
                    await asyncio.sleep(int(data))
                    writer.write(self.count_of_connections)

            except Exception as error:
                from server.exceptions import SomeException
                raise SomeException(error)


if __name__ == '__main__':
    pass
