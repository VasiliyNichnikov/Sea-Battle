import socket
import json
from _thread import *


class Server:
    def __init__(self, player_id_1, player_id_2):
        self.player_id_1 = player_id_1
        self.player_id_2 = player_id_2

        # Храним информацию, которую нужно будет передать игроку
        self.save_dict_player_1 = {'function': 'processing'}
        self.save_dict_player_2 = {'function': 'processing'}

        self.current_player = self.player_id_1

    # Запуск сервера
    def start_server(self, conn):
        first_motion = False
        if self.current_player == self.player_id_1:
            first_motion = True
        conn.send(json.dumps({'player_id': self.current_player, 'first_motion': first_motion}).encode('utf-8'))
        self.current_player = self.player_id_2

        while True:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                print('end')
                conn.send(json.dumps({'end': 'goodbye', 'function': 'end'}).encode('utf-8'))
                break
            else:
                print("Received: " + reply)
                # Получение информации из json файла
                info = json.loads(reply)

                if 'get_info' in info.keys() and info['get_info'] is True:
                    # Если информация пришла от игрока 1
                    if info['player_id'] == self.player_id_1:
                        conn.sendall(json.dumps(self.save_dict_player_1).encode('utf-8'))
                        self.save_dict_player_1 = {'function': 'processing'}
                    # Иначе, если информация пришла от игрока 2
                    elif info['player_id'] == self.player_id_2:
                        conn.sendall(json.dumps(self.save_dict_player_2).encode('utf-8'))
                        self.save_dict_player_2 = {'function': 'processing'}
                else:
                    # Если информация пришла от игрока 1
                    if info['player_id'] == self.player_id_1:
                        self.save_dict_player_2 = info
                    # Иначе, если информация пришла от игрока 2
                    elif info['player_id'] == self.player_id_2:
                        self.save_dict_player_1 = info
                    conn.sendall(json.dumps({'success': 'ok'}).encode('utf-8'))

        print('Connection Closed')
        conn.close()


if __name__ == '__main__':
    server = Server(player_id_1='player_1', player_id_2='player_2')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.168.0.30', 5555))
    print('Waiting for a connection')
    sock.listen(2)

    while True:
        conn, addr = sock.accept()
        start_new_thread(server.start_server, (conn,))
