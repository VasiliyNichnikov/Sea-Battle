from AllConditions import ConditionShip

""" Класс корабля, отвечает за каждый корабль в игре """


class Ship:
    def __init__(self, list_blocks_ship):
        # Длина корабля
        self.len_ship = len(list_blocks_ship)
        # Список блоков, которые и создают корабль
        self.list_blocks_ship = list_blocks_ship
        # Состояние корабля
        self.condition_ship = ConditionShip.Afloat

        for block in self.list_blocks_ship:
            block.len_ship_which_block_located = len(list_blocks_ship)

    # Возвращает словарь с позициями блоков корабля
    def get_positions_blocks(self):
        pass
