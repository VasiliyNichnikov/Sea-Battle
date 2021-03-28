import flask
from flask import jsonify, request

blueprint = flask.Blueprint('api', __name__)


@blueprint.route('/getting_lobbies', methods=['GET', 'POST'])
def getting_lobbies():
    """
    Данная функция возвращает все лобби, которые на данный момент есть на сервер
    :return: None
    """
    return jsonify({'condition': 'success', 'list_lobbies': [{'name': 'Game', 'id': 'df34ff', 'lock': False},
                                                             {'name': 'Все ко мне', 'id': 'f34asdf', 'lock': True},
                                                             {'name': 'Game2', 'id': 'df3asm4ff', 'lock': False}]})
