import socket
import json
import time
from _thread import *


class Server:
    def __init__(self, player_id_1, player_id_2):
        self.player_id_1 = player_id_1
        self.player_id_2 = player_id_2
        self.current_player = self.player_id_1

    # Запуск сервера
    def start_server(self, conn):
        conn.send(str.encode(self.current_player))
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

                print(f"Player id - {info['player_id']}\n"
                      f"Function - {info['function']}\n"
                      f"Parameters - {info['parameters']}\n")
                conn.sendall(json.dumps({'success': 'ok', 'function': 'selected'}).encode('utf-8'))

        print('Connection Closed')
        conn.close()


if __name__ == '__main__':
    server = Server(player_id_1='player_1', player_id_2='player_2')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 5000))
    print('Waiting for a connection')
    sock.listen(2)

    while True:
        conn, addr = sock.accept()
        start_new_thread(server.start_server, (conn,))

    # open_json = json.loads(reply)
    # if open_json['condition'] == 'move':
    #     print(f"Двигаем объект к {open_json['position']}")
    #     conn.send(json.dumps({'success': 'ok'}).encode('utf-8'))
    # conn.close()

# try:
#     sock.bind((server, port))
# except socket.error as e:
#     print(str(e))
