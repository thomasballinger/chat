import sys
import select
import socket
import termios, fcntl, sys, os, select, socket, threading, time

# code that sets up stdin to be happen one key at a time

class CharacterAtATime(object):
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.oldterm = termios.tcgetattr(self.fd)
        newattr = self.oldterm[:]
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.fd, termios.TCSANOW, newattr)
        self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)
    def __exit__(self, *args):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)


class Keyboard(object):
    def __init__(self, where_to_send_keypresses):
        self.sock = where_to_send_keypresses
    def fileno(self):
        return sys.stdin.fileno()
    def on_read(self):
        c = sys.stdin.read(1)
        self.sock.send(c)
        print 'sending', c

class Connection(object):
    def __init__(self, sock):
        self.sock = sock
    def fileno(self):
        return self.sock.fileno()
    def on_read(self):
        print(self.sock.recv(1))

def main():
    with CharacterAtATime():
        client = socket.socket()
        client.connect(('localhost', 1234))
        client.setblocking(False)

        while True:
            ready_to_read, _, _ = select.select([Connection(client), Keyboard(client)], [], [])
            for r in ready_to_read:
                r.on_read()

        #loop_fovers()


    print('we have now exited the with statement')

if __name__ == '__main__':
    main()
