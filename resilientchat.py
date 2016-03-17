import select
import socket
import os

ips_by_socket = {}


def get_ip_blacklist():
    if os.path.exists('ipblacklist.txt'):
        return open('ipblacklist.txt').read().split()
    else:
        return []


def add_to_blacklist(ip):
    with open('ipblacklist.txt', 'a') as f:
        f.write(ip)


def main():

    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('', 1234))
    server.listen(5)

    clients = []

    while True:
        blacklist = get_ip_blacklist()
        ready_to_read, _, error = select.select(clients + [server], [], [])
        if error:
            print('errors:', error)
        for r in ready_to_read:
            if r is server:
                client, info = server.accept()
                print(info, 'just connected')
                clients.append(client)
                ips_by_socket[client] = info[0]
            else:
                msg = r.recv(1000)
                if msg == '':
                    r.close()
                    clients.remove(r)
                    msg = ips_by_socket[r] + ' disconnected'
                if ips_by_socket[client] in blacklist:
                    continue
                if msg.startswith('blacklist'):
                    try:
                        add_to_blacklist(msg.split()[1])
                    except:
                        pass
                for receiver in clients:
                    try:
                        #receiver.send('you sent a message: '+msg
                        #              if receiver is r
                        #              else ips_by_socket[client] + ': '+msg)
                        receiver.send(msg)
                        print(ips_by_socket[client], msg)
                    except socket.error:
                        continue


if __name__ == '__main__':
    main()
