from AllConditions import ConditionShip, ConditionBlock, ConditionAxisShip

""" Класс корабля, отвечает за каждый корабль в игре """


class Ship:
    def __init__(self, list_blocks_ship):
        # Длина корабля
        self.len_ship = len(list_blocks_ship)
        # Список блоков, которые и создают корабль
        self.list_blocks_ship = list_blocks_ship
        # Состояние корабля
        self.condition_ship = ConditionShip.Afloat
        # Ось расположения корабля
        self.axis_ship = self.__select_axis_ship()

        for block in self.list_blocks_ship:
            block.ship_class = self
            block.len_ship_which_block_located = self.len_ship
            block.axis_block = self.axis_ship
            block.block_start_ship = False
            block.block_end_ship = False

        if self.len_ship > 1:
            self.list_blocks_ship[0].block_start_ship = True
            self.list_blocks_ship[-1].block_end_ship = True

    # Определение оси корабля
    def __select_axis_ship(self):
        if self.len_ship > 1:
            block_1, block_2 = self.list_blocks_ship[:2]
            x1, y1 = block_1.number_block
            x2, y2 = block_2.number_block
            if abs(x1 - x2) > 0:
                return ConditionAxisShip.Horizontal
        return ConditionAxisShip.Vertical

    # Возвращает словарь с позициями блоков корабля
    def get_positions_blocks(self):
        return [block.number_block for block in self.list_blocks_ship]

    # Проверяем уничтожен корабль или нет
    def check_condition_ship(self):
        for block in self.list_blocks_ship:
            if block.condition_block == ConditionBlock.Selected:
                return True
        return False


