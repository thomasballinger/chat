import select
import socket
import os
from collections import defaultdict

ips_by_socket = {}
events = []

buffers_by_socket = defaultdict(list)


def log(*stuff):
    events.append(stuff)
    print stuff


def get_ip_blacklist():
    if os.path.exists('ipblacklist.txt'):
        return open('ipblacklist.txt').read().split()
    else:
        return []


def add_to_blacklist(ip):
    log('blacklisted', ip)
    with open('ipblacklist.txt', 'a') as f:
        f.write(ip)
        f.write('\n')


def main():

    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 1234))
    server.listen(5)

    clients = []

    while True:
        blacklist = get_ip_blacklist()
        ready_to_read, _, _ = select.select(clients + [server], [], [])
        for r in ready_to_read:
            if r is server:
                client, info = server.accept()
                log(info, 'just connected')
                clients.append(client)
                ips_by_socket[client] = info[0]
            else:
                msg = r.recv(1000)
                if msg == '':
                    r.close()
                    clients.remove(r)
                    msg = ips_by_socket[r] + ' disconnected'
                if ips_by_socket[client] in blacklist:
                    log('blacklisted user', ips_by_socket[client], 'tried to send', msg)
                    continue

                buffers_by_socket[client] += msg
                if '\n' not in buffers_by_socket[client]:
                    continue

                msg = buffers_by_socket[client]
                buffers_by_socket[client] = ''

                if msg.startswith('blacklist'):
                    try:
                        add_to_blacklist(msg.split()[1])
                    except:
                        pass
                    continue
                if msg.startswith('log'):
                    r.sendall(repr(events[-100:]))
                    continue
                for receiver in clients:
                    try:
                        #receiver.send('you sent a message: '+msg
                        #              if receiver is r
                        #              else ips_by_socket[client] + ': '+msg)
                        receiver.send(msg)
                        log(ips_by_socket[client], msg)
                    except socket.error:
                        continue


if __name__ == '__main__':
    main()
