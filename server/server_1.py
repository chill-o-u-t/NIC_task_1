import asyncio
import logging

import utils


log = logging.getLogger(__name__)

clients = {}


def accept_clients(client_reader, client_writer):
    task = asyncio.Task(handle_client)
    clients[task] = (client_reader, client_writer)

    def clent_done(task):
        del clients[task]
        client_writer.close()


@asyncio.coroutine
def handle_client(client_reader, client_writer):
    data = yield from asyncio.wait_for(client_reader, timeout=10.0)
    pass


def main():
    from logger_config import *
    logger_conf()
