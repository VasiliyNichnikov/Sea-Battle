import pygame
from requests import Session
import sys
# Пустой объект
from scripts.draw_objects.empty import Empty
# Блок лобби
from scripts.lobby.lobbyBlock import LobbyBlock
# Позиция объектов
from scripts.position.positioning_operation import PositioningOperation, PositionAndSize, SelectPositioning
# Изображения
from scripts.images.image import Image
# Дополнительные параметры
from scripts.colorsParameters import WHITE
from scripts.main.mainParameters import FPS, BACKGROUND_MENU_LOBBY
from scripts.lobby.lobbyParameters import HEIGHT_BLOCK, DISTANCE_BETWEEN_BLOCKS, ANIMATION_SPEED


class Lobby(PositioningOperation):
    def __init__(self, parent: PositionAndSize, selected_positioning: SelectPositioning, height: int, width: int):
        super().__init__(parent, selected_positioning, height, width)
        pygame.init()
        self.__creating_screen()
        condition, values = self.__connecting_server()

        self.background = Image(surface=self.surface, path=BACKGROUND_MENU_LOBBY, parent=self,
                                selected_positioning=SelectPositioning.center,
                                height=self.height, width=self.width)

        if condition:
            # Максимальное кол-во блоков лобби
            self.max_blocks = len(values['list_lobbies'])

            self.parent_blocks_lobbies = Empty(surface=self.surface, parent=self,
                                               selected_positioning=SelectPositioning.up,
                                               width=self.width - 10,
                                               height=(HEIGHT_BLOCK + DISTANCE_BETWEEN_BLOCKS) * self.max_blocks,
                                               shift_y=HEIGHT_BLOCK, outline=2)

            self.__initializing_blocks(values)

        # Создание кнопки, которая отвечает за создание сервера
        # self.button_create_server = Button(self.surface, 2, 2, (0, 0, 0), 'Создать сервер', (255, 255, 255),
        #                                    path_font=path_font, size_font=30)
        # Создание блока лобби
        # self.creating_lobby = CreatingLobby(self.surface, 400, 400)
        # Задний фон лобби
        # self.background_image = load_image(path_background_menu, size_x=screen_width,
        #                                    size_y=screen_height, select_size=False)

        # self.test_text = Text(surface=self.surface, text='Test', size_font=40, color=(0, 0, 0), path_font=path_font,
        #                       parent=self,
        #                       selected_positioning=SelectPositioning.left_down)

    def __creating_screen(self):
        self.FPS = FPS
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Sea Battle')
        self.surface.fill(WHITE)
        # print(type(self.surface))

    def __connecting_server(self) -> (bool, str):
        session = Session()
        get_lobbies = session.get('http://127.0.0.1:5002/getting_lobbies')

        if get_lobbies.status_code == 200:
            return True, get_lobbies.json()
        return False, None

    def __initializing_blocks(self, values):
        self.blocks_lobby = [
            LobbyBlock(surface=self.surface, name=values['list_lobbies'][lobby_index]['name'], index=lobby_index,
                       parent=self.parent_blocks_lobbies, width=self.parent_blocks_lobbies.width,
                       height=HEIGHT_BLOCK,
                       shift_y=HEIGHT_BLOCK * lobby_index + DISTANCE_BETWEEN_BLOCKS * lobby_index,
                       lock=values['list_lobbies'][lobby_index]['lock'], selected_positioning=SelectPositioning.up)
            for lobby_index in range(self.max_blocks)]
        # Выбранный блок лобби (номер)
        self.select_number_block = 0

    def start_lobby(self):
        while True:
            # Background -----------------------------------------------------------------------------------------------
            self.background.draw()
            self.parent_blocks_lobbies.draw()

            # Отрисовка блоков
            # y = size_field_top + distance_between_block_lobby - (
            #         block_lobby + distance_between_block_lobby) * self.select_number_block

            for block_lobby in self.blocks_lobby:
                block_lobby.draw()

            # for lobby in self.list_objects_lobbies:
            #     line_y = 0
            #     block_select = False
            #     if self.select_number_block == lobby.get_index():
            #         block_select = True
            #         line_y = 10
            #     lobby.draw_block(y, block_select)
            #     y += block_lobby + distance_between_block_lobby + line_y
            # pygame.draw.rect(self.surface, COLOR_TOP_BLOCK, (0, 0, screen_width, size_field_top))
            # self.button_create_server.draw_button(screen_width - self.button_create_server.width - 5,
            #                                       size_field_top // 2 - self.button_create_server.height // 2)
            # Отрисовка создания лобби
            # if self.creating_lobby.draw_block:
            #     self.creating_lobby.draw(screen_width // 2 - self.creating_lobby.width // 2,
            #                              screen_height // 2 - self.creating_lobby.height // 2)
            # Events ---------------------------------------------------------------------------------------------------
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.parent_blocks_lobbies.move(shift_y=ANIMATION_SPEED)
                        # print("Прокручивание вперед")
                    elif event.button == 5:
                        self.parent_blocks_lobbies.move(shift_y=-ANIMATION_SPEED)
                        # print("Прокручивание назад")
                        # self.parent_blocks_lobbies.move(shift_y=self.parent_blocks_lobbies.y - 0.1)

                # if event.type == pygame.MOUSEWHEEL:
                #     print('Прокрутка колесика мыши')
                #     if not self.creating_lobby.draw_block:
                #         if self.list_objects_lobbies[self.select_number_block].lock:
                #             block = self.list_objects_lobbies[self.select_number_block]
                #             if event.key == pygame.K_RETURN:
                #                 print(block.text_password)
                #             elif event.key == pygame.K_BACKSPACE:
                #                 block.text_password = block.text_password[:-1]
                #             else:
                #                 block.text_password += event.unicode
                #
                #         if event.key == pygame.K_UP and self.select_number_block - 1 >= 0:
                #             self.select_number_block -= 1
                #         if event.key == pygame.K_DOWN and self.select_number_block + 1 < self.max_blocks:
                #             self.select_number_block += 1
                #     else:
                #         self.creating_lobby.entering_values(event)
                #
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if self.button_create_server.check_input_button(event.pos, True):
                #         self.creating_lobby.draw_block = not self.creating_lobby.draw_block
                #     if self.creating_lobby.draw_block:
                #         self.creating_lobby.input_block(event)

            self.clock.tick(FPS)
            pygame.display.update()
