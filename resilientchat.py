import select
import socket
import sys

ips_by_socket = {}

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 1234))
    server.listen(5)

    clients = []

    while True:
        try:
            ready_to_read, _, _ = select.select(clients + [server], [], [])
        except socket.error:
            ready_to_read = []
        for r in ready_to_read:
            if r is server:
                try:
                    client, info = server.accept()
                except socket.error:
                    continue
                print(info, 'just connected')
                clients.append(client)
                ips_by_socket[client] = info[0]
            else:
                try:
                    msg = r.recv(1000)
                    if msg == '':
                        r.close()
                        msg = ips_by_socket[r] + ' disconnected'

                except socket.error:
                    continue
                for receiver in clients:
                    try:
                        receiver.send('you sent a message: '+msg
                                      if receiver is r
                                      else ips_by_socket[client] + ': '+msg)
                    except socket.error:
                        continue


if __name__ == '__main__':
    main()
