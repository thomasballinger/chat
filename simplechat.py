import select
import sys
import socket

s = socket.socket()
s.connect(('localhost', 1234))

while True:
    ready, _, _ = select.select([s, sys.stdin], [], [])
    for r in ready:
        if r is sys.stdin:
            msg = sys.stdin.readline()
            if msg == '':
                print 'disconnected'
                sys.exit()
            s.send(msg)
        else:
            print r.recv(1000)
