import pygame
import sys
from colorsAndMainParameters import screen_height, screen_width, path_background_menu, path_font, FPS
from colorsAndMainParameters import SEA_WATER, WHITE, BLACK
from imagesAndAnimations import load_image
from textAndButtonAndInputPanel import SelectText, Text
from allConditions import ConditionButton


class Menu:
    def __init__(self):
        self.FPS = FPS

        pygame.init()
        self.surface = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Sea Battle')
        self.surface.fill(WHITE)

        # Задний фон меню
        self.background_image = load_image(path_background_menu, width=screen_width,
                                           height=screen_height, proportionately=False)

        # Вход в лобби
        self.play_btn = SelectText(self.surface, 'PLAY', 70, anti_aliasing=True, path_font=path_font,
                                   color_select=BLACK,
                                   color_default=SEA_WATER, select_text_obj=True, condition_button=ConditionButton.Play)
        # Кнопка выхода из игры
        self.exit_btn = SelectText(self.surface, 'EXIT', 70, anti_aliasing=True, path_font=path_font,
                                   color_select=BLACK,
                                   color_default=SEA_WATER, condition_button=ConditionButton.Exit)

        # Название игры
        self.name_game_text = Text(self.surface, 'SEA BATTLE', 100, WHITE, anti_aliasing=True, path_font=path_font)

        self.selected_index_btn = 0
        self.list_buttons = [self.play_btn, self.exit_btn]

        for index_btn in range(len(self.list_buttons)):
            if self.list_buttons[index_btn].select_text_obj:
                self.selected_index_btn = index_btn
                break

    @staticmethod
    def exit_game():
        pygame.quit()
        sys.exit()

    def start_menu(self):
        while True:
            # Background -----------------------------------------------------------------------------------------------
            self.surface.fill(WHITE)
            self.surface.blit(self.background_image, (0, 0))
            # Текст, "Название игры"
            self.name_game_text.draw_text((screen_width // 2 - self.name_game_text.__object.get_width() // 2, 5))
            # Кнопка, "Зайти в лобби"
            self.play_btn.draw_text((screen_width // 2 - self.play_btn.text_obj.get_width() // 2,
                                     screen_height // 2 - self.play_btn.text_obj.get_height() // 2))
            # Кнопка, "Выйти из игры"
            self.exit_btn.draw_text((screen_width // 2 - self.exit_btn.text_obj.get_width() // 2,
                                     screen_height // 2 - self.exit_btn.text_obj.get_height() // 2
                                     + self.play_btn.text_obj.get_height()))
            # Events ---------------------------------------------------------------------------------------------------
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.exit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.selected_index_btn += 1
                        if self.selected_index_btn + 1 > len(self.list_buttons):
                            selected_index_btn = 0
                    if event.key == pygame.K_s:
                        self.selected_index_btn -= 1
                        if self.selected_index_btn < 0:
                            selected_index_btn = len(self.list_buttons) - 1

                    for btn in self.list_buttons:
                        btn.select_text_obj = False
                    selected_btn = self.list_buttons[self.selected_index_btn]
                    selected_btn.select_text_obj = True

                    if event.key == pygame.K_RETURN and selected_btn is not None:
                        if selected_btn.get_condition_button() == ConditionButton.Play:
                            self.surface = pygame.display.set_mode((1045, 555))
                        elif selected_btn.get_condition_button() == ConditionButton.Exit:
                            self.exit_game()

            self.clock.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    menu = Menu()
    menu.start_menu()
