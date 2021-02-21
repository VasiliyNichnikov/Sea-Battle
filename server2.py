from flask import Flask
from flask import jsonify
from enum import Enum

app = Flask(__name__)


class ConditionMotion(Enum):
    Player_1 = 0
    Player_2 = 1
    Player_None = 2


# Игрок 1
player_id_1 = None
# Игрок 2
player_id_2 = None
# Какой игрок сейчас ходит
condition_motion = ConditionMotion.Player_None


# Описание ошибок
# 1xx - ошибки со стороны игрока
# 101 - на сервере достаточно игроков
# 102 - на сервере не достаточно игроков
# 103 - игрок, который должен ходить не найден
# 104 - не верный user_id у игрока


# Проверка, что user_id есть среди двух игроков
def check_user_id(user_id) -> bool:
    global player_id_1, player_id_2
    if player_id_1 == user_id or player_id_2 == user_id:
        return True
    return False


@app.route('/login_player/<string:user_id>/', methods=['GET', 'POST'])
def login_player(user_id):
    global player_id_1, player_id_2
    if player_id_1 is None:
        player_id_1 = user_id
        return jsonify({'success': 'player_id_1 added', 'condition': True})
    elif player_id_2 is None and player_id_1 != user_id:
        player_id_2 = user_id
        return jsonify({'success': 'player_id_2 added', 'condition': True})
    return jsonify({'error': 'players found', 'error_id': 101, 'condition': False})


@app.route('/')
def test():
    return 'Hello World!'


# Проверяем можно или нет запускать игру
@app.route('/check_start_game/<string:user_id>/', methods=['GET', 'POST'])
def check_start_game(user_id):
    global condition_motion, player_id_1, player_id_2
    if check_user_id(user_id):
        if player_id_1 is not None and player_id_2 is not None:
            condition_motion = ConditionMotion.Player_1
            return jsonify({'success': 'start game', 'condition': True})
        return jsonify({'error': 'players found', 'error_id': 102, 'condition': False})
    return jsonify({'error': 'user_id not found', 'error_id': 104, 'condition': False})


# Возвращаем id игрока, который сейчас выполняет ход
@app.route('/get_player_motion/<string:user_id>/', methods=['GET', 'POST'])
def get_player_motion(user_id):
    global condition_motion, player_id_1, player_id_2
    if check_user_id(user_id):
        if condition_motion == ConditionMotion.Player_1:
            return jsonify({'success': 'player_1 motion', 'player_id': player_id_1, 'condition': True})
        elif condition_motion == ConditionMotion.Player_2:
            return jsonify({'success': 'player_2 motion', 'player_id': player_id_2, 'condition': True})
        else:
            return jsonify({'error': 'motion player not found', 'error_id': 103, 'condition': False})
    return jsonify({'error': 'user_id not found', 'error_id': 104, 'condition': False})


if __name__ == '__main__':
    app.run(port='1000')
