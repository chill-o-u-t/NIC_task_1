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

    def count_connections(self):
        r = 0
        return str(r)

    def FastResponse(self, writer):
        writer.write(time_now)

    def SlowResponse(self, writer, data):
        await asyncio.sleep(int(data))
        writer.write(self.count_connections)

    @asyncio.coroutine
    def handle_connection(self, reader, writer):
        # Я пока не понимаю, как обозначается при приеме данных, наличие аргумента
        # По идее, если data=None, то это fast, но не точно
        # Но сюда надо еще интегрировать протокол, и пока в душе не *** как
        # Пока что 1 и что 2
        what_1 = True
        what_2 = True
        while not reader.at_eof():
            try:
                data = yield from asyncio.wait_for(reader.readline(), timeout=None)
                writer.write(data)
                if what_1:
                    self.FastResponse(writer)
                if what_2:
                    self.SlowResponse(writer, data)
            except Exception as error:
                from server.exceptions import SomeException
                raise SomeException(error)


if __name__ == '__main__':
    pass
