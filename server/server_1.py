import asyncio

import utils


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    pass

async def main():
    server = await asyncio.start_server(
        handle_echo,
        utils.IP,
        utils.PORT
    )
    pass
