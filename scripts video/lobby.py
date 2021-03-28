import pygame
from requests import Session
import sys
from colorsAndMainParameters import screen_height, screen_width, path_background_menu, FPS, size_field_top, \
    block_lobby, distance_between_block_lobby, path_font
from colorsAndMainParameters import WHITE, COLOR_TOP_BLOCK, GREEN, RED, YANDEX_COLOR
from textAndButton import Text
from imagesAndAnimations import load_image


class Menu:
    def __init__(self):
        self.FPS = FPS

        pygame.init()
        self.surface = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Sea Battle')
        self.surface.fill(WHITE)

        self.list_lobbies = []

        session = Session()

        get_lobbies = session.get('http://127.0.0.1:5002/getting_lobbies')
        if get_lobbies.status_code == 200:
            self.list_lobbies = get_lobbies.json()['list_lobbies']

        # Максимальное кол-во блоков лобби
        self.max_blocks = len(self.list_lobbies)
        # Выбранный блок лобби
        self.select_number_block = 0

        # Задний фон меню
        self.background_image = load_image(path_background_menu, size_x=screen_width,
                                           size_y=screen_height, select_size=False)

    def start_menu(self):
        while True:
            # Background -----------------------------------------------------------------------------------------------
            self.surface.fill(WHITE)
            self.surface.blit(self.background_image, (0, 0))

            y = size_field_top + distance_between_block_lobby - (
                    block_lobby + distance_between_block_lobby) * self.select_number_block
            for lobby_index in range(len(self.list_lobbies)):
                # Создание текста лобби
                name_lobby = Text(self.surface, self.list_lobbies[lobby_index]['name'], 30, COLOR_TOP_BLOCK, anti_aliasing=True,
                                  path_font=path_font)
                color_circle = GREEN
                color_block = WHITE

                if lobby_index == self.select_number_block:
                    color_block = YANDEX_COLOR

                pygame.draw.rect(self.surface, color_block,
                                 (distance_between_block_lobby, y,
                                  screen_width - distance_between_block_lobby * 2, block_lobby))

                if self.list_lobbies[lobby_index]['lock']:
                    color_circle = RED

                pygame.draw.circle(self.surface, color_circle,
                                   (screen_width - distance_between_block_lobby * 5, y + block_lobby // 2),
                                   block_lobby // 4)

                # Отрисовка названия лобби
                name_lobby.draw_text(
                    position=(distance_between_block_lobby * 2, y + name_lobby.text_obj.get_height() // 2))
                # Отрисовка состояния лобби

                y += block_lobby + distance_between_block_lobby
            pygame.draw.rect(self.surface, COLOR_TOP_BLOCK, (0, 0, screen_width, size_field_top))
            # Events ---------------------------------------------------------------------------------------------------
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and self.select_number_block - 1 >= 0:
                        self.select_number_block -= 1
                    if event.key == pygame.K_s and self.select_number_block + 1 < self.max_blocks:
                        self.select_number_block += 1

            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    menu = Menu()
    menu.start_menu()
