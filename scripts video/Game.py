from Map import Map
from AllConditions import ConditionMap
from ColorsAndMainParameters import WHITE
from ColorsAndMainParameters import height, width, distance_between_maps, border, distance_screen_up_maps
import pygame


class Game:
    def __init__(self):
        # Создание карты
        def create_map(name, condition_map):
            new_map = Map(name=name, condition_map=condition_map, surface=self.surface)
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
        create_map('Player', ConditionMap.Player)
        # Создание карты противника
        create_map('Enemy', ConditionMap.Enemy)

    # Запуск игры
    def start_game(self):
        while self.runner:
            self.clock.tick(self.FPS)

            # Отрисовка карты
            for select_map in self.list_maps:
                select_map.draw_map()

            # if player_logged:
            #     draw_map()
            #
            #     text_player = get_text('PLAYER', 40, BLUE_AZURE, True, path_font)
            #     surface.blit(text_player, (border + width // 2 - text_player.get_width() // 2,
            #                                shift_along_axis_y // 2 - text_player.get_height() // 2 + border))
            #
            #     text_enemy = get_text('ENEMY_251', 40, RED, True, path_font)
            #     surface.blit(text_enemy,
            #                  (border + width // 2 - text_enemy.get_width() // 2 + width + distance_between_maps,
            #                   shift_along_axis_y // 2 - text_enemy.get_height() // 2 + border))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runner = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pass
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass

            pygame.display.flip()
        self.surface.fill(WHITE)


if __name__ == '__main__':
    game = Game()
    game.start_game()
