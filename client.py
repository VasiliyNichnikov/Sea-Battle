import socket
import json

sock = socket.socket()

try:
    sock.connect(('localhost', 5555))

    info = {'position': (10, 10), 'condition': 'move'}

    sock.send(json.dumps(info).encode('utf-8'))

    data = sock.recv(2048)
    sock.close()

    print(data)
except ConnectionRefusedError as e:
    print('Ошибка подключения к серверу - %s' % e)