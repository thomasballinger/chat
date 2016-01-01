import sys
import select
import socket

def main():

    server = socket.socket()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 1234))
    server.listen(5)

    clients = []

    while True:
        ready_to_read, _, _ = select.select(clients + [server], [], [])
        for r in ready_to_read:
            if r is server:
                s, addr = server.accept()
                print(addr, 'just connected')
                clients.append(s)
            else:
                msg = r.recv(1000)
                for client in clients:
                    if client is not r:
                        client.send(msg)

if __name__ == '__main__':
    main()
