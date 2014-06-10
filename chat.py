import asyncio
import urllib.parse
import sys
import os

from oldchat import CharacterAtATime

def red_on_blue(msg):
    sys.stdout.write('\x1b[31m\x1b[44m' + msg + '\x1b[49m\x1b[39m')
    sys.stdout.flush()

def blue_on_red(msg):
    sys.stdout.write('\x1b[34m\x1b[41m' + msg + '\x1b[49m\x1b[39m')
    sys.stdout.flush()

class Input(object):
    def __init__(self):
        self.unprocessed = []
    def get_key(self):
        """Returns None if no keypress is yet available"""
        data = os.read(sys.stdin.fileno(), 1000)
        keys = {
                b'\x1b[A':'<RIGHT>',
                b'\x1b[B':'<DOWN>',
                b'\x1b[C':'<RIGHT>',
                b'\x1b[D':'<LEFT>',
               }
        if data in keys:
            e = keys[data]
        else:
            e = data.decode('utf8')
        print('os.read bytes:', repr(data), 'so returning', e)
        return e

@asyncio.coroutine
def listen_to_server(reader):
    while True:
        c = yield from reader.read(1)
        if not c:
            break
        blue_on_red(c.decode('utf8'))

@asyncio.coroutine
def connect(loop):
    server_reader, server_writer = yield from asyncio.open_connection('localhost', 1234)

    asyncio.async(listen_to_server(server_reader))
    in_gen = Input()
    def on_stdin_read():
        c = in_gen.get_key()
        if c is None:
            return
        red_on_blue(c)
        server_writer.write(c.encode('utf8'))
    loop.add_reader(sys.stdin, on_stdin_read)

loop = asyncio.get_event_loop()
asyncio.async(connect(loop))

with CharacterAtATime():
    loop.run_forever()
