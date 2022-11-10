import asyncio
import logging
import os

from server.utils import time_now


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

    def qbytearray_to_string(self, object) -> float:
        data_code = 0 # Будет функция перевода
        return data_code

    def fast_response(self, writer):
        object = time_now # Далее перевод в QByteArray
        writer.write(object)

    async def slow_response(self, writer, data):
        await asyncio.sleep(int(data))
        object = '' # Перевод строки в QByteArray
        writer.write(object)

    async def handle_connection(self, reader, writer):
        while not reader.at_eof():
            import concurrent
            try:
                data = ''
                #data = yield from asyncio.wait_for(reader.readline(), timeout=None)
                data_code = self.qbytearray_to_string(data)
                if data_code == 0:
                    self.fast_response(writer)
                elif 10 <= data_code <= 1000:
                    self.slow_response(writer, data_code)
                else:
                    logging.error('Недопустимое время дилея')
            except concurrent.futures.TimeoutError:
                logging.critical('Превышено время ожидания')
                break


if __name__ == '__main__':
    server = EchoServer(os.getenv('SERVER_IP'), os.getenv('DEFAULT_PORT'))
    logging.info(
        'Создан сервер: {host}:{port}'.format(
            host=os.getenv('SERVER_IP'),
            port=os.getenv('DEFAULT_PORT')
        )
    )
    try:
        server.start_server()
        logging.info('Сервер запущен')
    except KeyboardInterrupt:
        pass # ctrl + c
    finally:
        server.close_server()
        logging.info('Сервер выключен')
