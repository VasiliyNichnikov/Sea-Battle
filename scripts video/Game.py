from Map import Map
from AllConditions import ConditionMap, ConditionFunctionMap
from TextAndButton import Text
from ColorsAndMainParameters import WHITE, BLUE_AZURE, RED
from ColorsAndMainParameters import height, width, distance_between_maps, border, distance_screen_up_maps, path_font, \
    path_json_player
import json
import pygame


class Game:
    def __init__(self):
        # Создание карты
        def create_map(name, condition_map, list_json_file=None):
            new_map = Map(name=name, condition_map=condition_map, surface=self.surface, list_json_file=list_json_file)
            self.list_maps.append(new_map)

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
        create_map('Player', ConditionMap.Player, self.__open_json(path_json_player)['description'])
        # Создание карты противника
        create_map('Enemy', ConditionMap.Enemy)
        # Создание текста
        self.nickname_player_text = Text(self.surface, 'PLAYER', 40, BLUE_AZURE, True, path_font)
        self.nickname_enemy_text = Text(self.surface, 'ENEMY_258', 40, RED, True, path_font)

    # Запуск функции в классе Map
    def start_function_map(self, condition_function_map, **kwargs):
        for select_map in self.list_maps:
            if condition_function_map == ConditionFunctionMap.Draw_Map:
                select_map.draw_map()
            elif condition_function_map == ConditionFunctionMap.Check_Input_Mouse:
                select_map.check_input_map(kwargs['position_mouse'])

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

            pygame.display.flip()
        self.surface.fill(WHITE)


if __name__ == '__main__':
    game = Game()
    game.start_game()
