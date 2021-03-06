""" Хранит константы цветов и основные параметры"""

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE_AZURE = (42, 82, 190)
GREEN = (0, 128, 0)
YANDEX_COLOR = (255, 204, 0)
SEA_WATER = (0, 102, 170)


# Основные параметры
# Размеры карты
height = width = 500
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
path_font = '../Fonts/main_font.otf'
# Путь до карты игрока в виде json файла
path_json_player = '../static/map_player.json'
