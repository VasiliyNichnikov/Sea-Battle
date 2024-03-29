# from map import Map
# from allConditions import ConditionPlayerMap, ConditionFunctionMap, ConditionShip
# from textAndButtonAndInputPanel import Text
from scripts.game.map.map import Map
from scripts.colorsAndMainParameters import WHITE, BLUE_AZURE, RED
from scripts.game.map.parametersMap import ParametersMap
from scripts.colorsAndMainParameters import block_size, number_blocks
from scripts.colorsAndMainParameters import height, width, distance_between_maps, border, distance_screen_up_maps, \
    path_font, \
    path_json_player, FPS
# from connectServer import ConnectServer
from scripts.game.map.condition import EnumMap
from scripts.colorsAndMainParameters import number_blocks, block_size
import json
import pygame
from pygame import Vector2


class Game:
    def __init__(self):
        def create_map(parameters_map: ParametersMap):
            new_map = Map(parameters_map)
            # self.maps.append(new_map)
            return new_map

        # self.connect_server = ConnectServer(host='localhost', port=5000)  # player_id=player_id,
        # self.player_id = self.connect_server.player_id
        # self.first_motion = self.connect_server.first_motion

        # self.condition_motion = ConditionPlayerMap.Player
        # if not self.first_motion:
        #     self.condition_motion = ConditionPlayerMap.Enemy

        self.FPS = FPS
        self.runner = True
        self.maps = []

        # Инициализация игры
        pygame.init()
        self.surface = pygame.display.set_mode((width * 2 + distance_between_maps + border,
                                                height + distance_screen_up_maps + border))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Sea Battle')
        self.surface.fill(WHITE)

        self.player_map = create_map(ParametersMap('Player',
                                                   self.surface,
                                                   condition=EnumMap.Player,
                                                   size=Vector2(number_blocks * block_size, number_blocks * block_size),
                                                   border=Vector2(border, distance_screen_up_maps)))

        self.enemy_map = create_map(ParametersMap('Enemy',
                                                  self.surface,
                                                  condition=EnumMap.Enemy,
                                                  size=Vector2(number_blocks * block_size, number_blocks * block_size),
                                                  border=Vector2(distance_between_maps + width, distance_screen_up_maps)))

        # self.player_map = create_map('Player', ConditionPlayerMap.Player,
        #                              self.__open_json(path_json_player)['description'])
        # Создание карты противника
        # self.enemy_map = create_map('Enemy', ConditionPlayerMap.Enemy)
        # Создание текста
        # self.nickname_player_text = Text(self.surface, 'PLAYER', 40, BLUE_AZURE, True, path_font)
        # self.nickname_enemy_text = Text(self.surface, 'ENEMY_258', 40, RED, True, path_font)

    # Запуск функции в классе Map
    # def start_function_map(self, condition_function_map, **kwargs):
    #     for select_map in self.list_maps:
    #         if condition_function_map == ConditionFunctionMap.DrawMap:
    #             select_map.draw_map(self.condition_motion)
    #         elif condition_function_map == ConditionFunctionMap.CheckInputMouse:
    #             block = select_map.get_block_input_map(kwargs['position_mouse'])
    #             if block is not None and self.condition_motion == ConditionPlayerMap.Player:
    #                 # Отправка информации на сервер
    #                 self.connect_server.send({'player_id': self.player_id,
    #                                           'function': 'attack',
    #                                           'parameters': {'block': block.number_block}})

    # Открытие json файла
    def __open_json(self, path_map) -> dict:
        with open(path_map, 'r', encoding='utf-8') as read_file:
            data = json.load(read_file)
        return data

    # Проверяем сервер
    # def check_server(self) -> None:
    #     # Ответ от сервера
    #     answer = self.connect_server.send({'player_id': self.player_id, 'get_info': True})
    #     if answer['function'] != 'processing':
    #         # Позиция блока
    #         position_block = answer['parameters']['block']
    #         # Противник атакует игрока
    #         if answer['function'] == 'attack':
    #             # Получаем блок с карты игрока
    #             block = self.player_map.get_block_using_position(position_block)
    #             condition_ship = True
    #             positions_blocks_ship = []
    #             function_block = block.check_condition_block()
    #
    #             if block.ship_class is not None:
    #                 select_ship = block.ship_class
    #                 condition_ship = select_ship.check_condition_ship()
    #                 positions_blocks_ship = select_ship.get_positions_blocks()
    #                 if not condition_ship:
    #                     self.player_map.draw_ships_blocks(select_ship.list_blocks_ship)
    #                     select_ship.condition_ship = ConditionShip.Destroyed
    #                     print('Корабль уничтожен, закрашиваем поле')
    #             else:
    #                 # Должна быть ошибка
    #                 pass
    #
    #             if function_block['next_motion']:
    #                 self.condition_motion = ConditionPlayerMap.Player
    #             self.connect_server.send({'player_id': self.player_id, 'function': function_block['function'],
    #                                       'parameters': {'block': position_block, 'ship_condition': condition_ship,
    #                                                      'positions_blocks_ship': positions_blocks_ship}})
    #         # Игрок атакует противника
    #         else:
    #             # Получем блок с карты противника
    #             block = self.enemy_map.get_block_using_position(position_block)
    #             if answer['function'] == 'hit':
    #                 block.change_to_hit()
    #                 if not answer['parameters']['ship_condition']:
    #                     list_blocks = [self.enemy_map.get_block_using_position(pos)
    #                                    for pos in answer['parameters']['positions_blocks_ship']]
    #                     self.enemy_map.create_ship(list_blocks)
    #                     self.enemy_map.draw_ships_blocks(list_blocks)
    #                     print('Корабль противника уничтожен,', answer['parameters']['positions_blocks_ship'])
    #
    #             elif answer['function'] == 'miss':
    #                 self.condition_motion = ConditionPlayerMap.Enemy
    #                 block.change_to_miss()

    # Запуск игры
    def start_game(self):
        while self.runner:
            self.clock.tick(self.FPS)

            self.player_map.draw()
            self.enemy_map.draw()

            # Отрисовка карты
            # self.start_function_map(ConditionFunctionMap.DrawMap)

            # Отрисовка текста
            # self.nickname_player_text.draw_text(
            #     position=(border + width // 2 - self.nickname_player_text.__object.get_width() // 2,
            #               distance_screen_up_maps // 2 - self.nickname_player_text.__object.get_height() // 2 - border)
            # )
            # self.nickname_enemy_text.draw_text(
            #     position=(
            #         border + width // 2 - self.nickname_enemy_text.__object.get_width() // 2 + width + distance_between_maps,
            #         distance_screen_up_maps // 2 - self.nickname_enemy_text.__object.get_height() // 2 - border)
            # )
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runner = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pass
                        # self.start_function_map(ConditionFunctionMap.CheckInputMouse, position_mouse=event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass

            # Работа с сервером
            # self.check_server()

            pygame.display.flip()
        self.surface.fill(WHITE)


if __name__ == '__main__':
    game = Game()
    game.start_game()
