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


def main():
    with CharacterAtATime():
        client = socket.socket()
        client.connect(('localhost', 1234))
        client.setblocking(False)

        while True:
            ready_to_read, _, _ = select.select([client, sys.stdin], [], [])
            for r in ready_to_read:
                if r == sys.stdin:
                    c = sys.stdin.read(1)
                    print c
                    client.send(c)
                elif r is client:
                    print client.recv(1)

    print 'we have now exited the with statement'


main()
