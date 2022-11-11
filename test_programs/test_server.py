import asyncio

HOST = '127.0.0.1'
PORT = 9999


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while reader.at_eof():
        data = await reader.read(1024)
        m = data.decode()

        addr, port = writer.get_extra_info('peername')
        print(f'{addr}:{port} - {m}')
        writer.write(data)
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def start_server():
    server = await asyncio.start_server(handle_echo, HOST, PORT)
    print('start server {host}:{port}'.format(host=HOST, port=PORT))
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_server())
