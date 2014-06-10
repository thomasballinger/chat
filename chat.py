import asyncio
import urllib.parse
import sys

from oldchat import CharacterAtATime

@asyncio.coroutine
def listen_to_server(reader):
    while True:
        line = yield from reader.read(1)
        if not line:
            break
        print('line:', line)

@asyncio.coroutine
def connect(loop):
    server_reader, server_writer = yield from asyncio.open_connection('localhost', 1234)

    asyncio.async(listen_to_server(server_reader))
    def on_stdin_read():
        print('reading on stdin')
        server_writer.write(sys.stdin.readline().encode('ascii'))
    loop.add_reader(sys.stdin, on_stdin_read)

loop = asyncio.get_event_loop()
asyncio.async(connect(loop))

with CharacterAtATime():
    loop.run_forever()
