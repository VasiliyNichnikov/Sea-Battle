import flask
from flask import jsonify, request

blueprint = flask.Blueprint('api', __name__)


@blueprint.route('/getting_lobbies', methods=['GET', 'POST'])
def getting_lobbies():
    """
    Данная функция возвращает все лобби, которые на данный момент есть на сервер
    :return: None
    """
    return jsonify({'condition': 'success', 'list_lobbies': [{'name': 'game', 'id': 'df34ff', 'lock': False},
                                                             {'name': 'Все ко мне', 'id': 'f34asdf', 'lock': True},
                                                             {'name': 'Game2', 'id': 'df3asm4ff', 'lock': False},
                                                             {'name': 'Game3', 'id': 'hello', 'lock': False},
                                                             {'name': 'Game4', 'id': 'world', 'lock': True},
                                                             {'name': 'Game5', 'id': 'world2', 'lock': False},
                                                             {'name': 'Game6', 'id': 'hefdf', 'lock': True},
                                                             {'name': 'Game7', 'id': 'world2', 'lock': False},
                                                             {'name': 'Game8', 'id': 'world2', 'lock': False},
                                                             {'name': 'Game9', 'id': 'world2', 'lock': False},
                                                             {'name': 'Game10', 'id': 'world2', 'lock': False}]})
