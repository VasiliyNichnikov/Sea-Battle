from Map import Map
from AllConditions import ConditionPlayerMap, ConditionFunctionMap
from TextAndButton import Text
from ColorsAndMainParameters import WHITE, BLUE_AZURE, RED
from ColorsAndMainParameters import height, width, distance_between_maps, border, distance_screen_up_maps, path_font, \
    path_json_player
from ConnectServer import ConnectServer
import json
import pygame


class Game:
    def __init__(self):
        # Создание карты
        def create_map(name, condition_player_map, list_json_file=None):
            new_map = Map(name=name, condition_player_map=condition_player_map, surface=self.surface,
                          list_json_file=list_json_file)
            self.list_maps.append(new_map)

        # id игрока
        # self.player_id = player_id
        # Подключение к серверу
        self.connect_server = ConnectServer(host='25.68.177.81', port=5000)  # player_id=player_id,
        self.player_id = self.connect_server.player_id
        # Кто из игроков сейчас ходит
        self.condition_motion = ConditionPlayerMap.Player

        # Кол-во FPS
        self.FPS = 60
        # Запущена игра или нет
        self.runner = True
        # Карты
        self.list_maps = []

        # Инициализация игры
        pygame.init()
        self.surface = pygame.display.set_mode((width * 2 + distance_between_maps + border,
                                                height + distance_screen_up_maps + border))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Sea Battle')
        self.surface.fill(WHITE)

        # Создание карты игрока
        create_map('Player', ConditionPlayerMap.Player, self.__open_json(path_json_player)['description'])
        # Создание карты противника
        create_map('Enemy', ConditionPlayerMap.Enemy)
        # Создание текста
        self.nickname_player_text = Text(self.surface, 'PLAYER', 40, BLUE_AZURE, True, path_font)
        self.nickname_enemy_text = Text(self.surface, 'ENEMY_258', 40, RED, True, path_font)

    # Запуск функции в классе Map
    def start_function_map(self, condition_function_map, **kwargs):
        for select_map in self.list_maps:
            if condition_function_map == ConditionFunctionMap.Draw_Map:
                select_map.draw_map()
            elif condition_function_map == ConditionFunctionMap.Check_Input_Mouse:
                block = select_map.get_block_input_map(kwargs['position_mouse'])
                if block is not None:
                    # Отправка информации на сервер
                    self.connect_server.send({'player_id': self.player_id,
                                              'function': 'attack',
                                              'parameters': {'block': block.number_block}})
            elif condition_function_map == ConditionFunctionMap.Destroy_Block and \
                    select_map.condition_player_map == kwargs['condition_map']:
                block = select_map.get_block_using_position(kwargs['position_block'])
                block.change_to_hit()

    # Открытие json файла
    def __open_json(self, path_map) -> dict:
        with open(path_map, 'r', encoding='utf-8') as read_file:
            data = json.load(read_file)
        return data

    # Запуск игры
    def start_game(self):
        while self.runner:
            self.clock.tick(self.FPS)

            # Отрисовка карты
            self.start_function_map(ConditionFunctionMap.Draw_Map)

            # Отрисовка текста
            self.nickname_player_text.draw_text(
                position=(border + width // 2 - self.nickname_player_text.text.get_width() // 2,
                          distance_screen_up_maps // 2 - self.nickname_player_text.text.get_height() // 2 - border)
            )
            self.nickname_enemy_text.draw_text(
                position=(
                    border + width // 2 - self.nickname_enemy_text.text.get_width() // 2 + width + distance_between_maps,
                    distance_screen_up_maps // 2 - self.nickname_enemy_text.text.get_height() // 2 - border)
            )

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runner = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.start_function_map(ConditionFunctionMap.Check_Input_Mouse, position_mouse=event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
            # Работа с сервером
            answer = self.connect_server.send({'player_id': self.player_id, 'get_info': True})
            if answer['function'] != 'processing':
                if answer['function'] == 'attack':
                    position_block = answer['parameters']['block']
                    # print(f"Блок - {position_block} уничтожен")
                    self.connect_server.send({'player_id': self.player_id, 'function': 'destroyed',
                                              'parameters': {'block': position_block}})
                    self.start_function_map(ConditionFunctionMap.Destroy_Block, position_block=position_block,
                                            condition_map=ConditionPlayerMap.Player)
                elif answer['function'] == 'destroyed':
                    position_block = answer['parameters']['block']
                    self.start_function_map(ConditionFunctionMap.Destroy_Block, position_block=position_block,
                                            condition_map=ConditionPlayerMap.Enemy)
                # print(answer)
            pygame.display.flip()
        self.surface.fill(WHITE)


if __name__ == '__main__':
    game = Game()
    game.start_game()
