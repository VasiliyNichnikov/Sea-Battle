import socket
import json


class ConnectServer:
    def __init__(self, port, host='localhost'):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        player_id_and_first_motion = self.connect()
        self.player_id, self.first_motion = player_id_and_first_motion['player_id'], player_id_and_first_motion['first_motion']
        print(f'Id игрока - {self.player_id}; First Motion - {self.first_motion}')
        # print(self.player_id, self.)
        # print(f'Id - {self.id}')
        print('Подключение к серверу завершено')
        # Сделать проверку на ошибки, если нет интернета

    # Подключение к серверу
    def connect(self):
        self.client.connect(self.addr)
        print('Ожидание подключения')
        return json.loads(self.client.recv(2048).decode('utf-8'))

    # Отправка и получение данных с сервера
    def send(self, info):
        try:
            self.client.send(json.dumps(info).encode('utf-8'))
            reply = json.loads(self.client.recv(2048).decode('utf-8'))
            return reply
        except socket.error as e:
            return e
