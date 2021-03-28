""" Хранит константы цветов и основные параметры"""

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE_AZURE = (42, 82, 190)
GREEN = (0, 128, 0)
YANDEX_COLOR = (255, 204, 0)
SEA_WATER = (0, 102, 170)
# Цвет блока в лобби
COLOR_TOP_BLOCK = (103, 109, 122)
# Цвет текста блока
COLOR_GRAY_BLOCK = (66, 70, 83)


# Основные параметры
# Размеры карты
height = width = 500
# FPS
FPS = 60
# Размеры экраны
screen_height, screen_width = 500, 800
# Размер верхнего блока
size_field_top = 50
# Размер блока в лобби
block_lobby = 60
# Расстояние между блоками в лобби
distance_between_block_lobby = 5
# Расстояние между двумя картами
distance_between_maps = 40
# Расстояние между верхней точкой приложения и картой по оси y
distance_screen_up_maps = 50
# Границы
border = 5
# Кол-во блоков
number_blocks = 10
# Расстояние между блоками
distance_between_blocks = 2
# Размер одного блока
block_size = height // number_blocks
# Путь до шрифта
path_font = '../static/fonts/main_font.otf'
# Путь до карты игрока в виде json файла
path_json_player = '../static/map_player.json'
# Путь до заднего фона меню
path_background_menu = '../static/menu/background.png'
# Путь до изображения блока лобби (не нажатого)
path_block_lobby_not_pressed = '../static/lobby/lobby block (not pressed).png'
# Путь до изображения блока лобби (нажатого)
path_block_lobby_pressed = '../static/lobby/lobby block (pressed).png'
# Путь до изображения выделения текста
path_text_selection = '../static/lobby/text selection.png'
