from enum import Enum

""" Состояния различных компонентов игры"""


# Состояние карты игрока
class ConditionPlayerMap(Enum):
    Player = 0
    Enemy = 1


# Состояние карты
class ConditionMap(Enum):
    Default = 0
    Lock = 1


# Функция, которую нужно запустить у карты
class ConditionFunctionMap(Enum):
    Draw_Map = 0
    Check_Input_Mouse = 1


# Состояние корабля
class ConditionShip(Enum):
    Afloat = 0
    Destroyed = 1


# Состояние блока
class ConditionBlock(Enum):
    Empty = 0
    Selected = 1
    Lock = 2
    Miss = 3
    Hit = 4


# Состояние кто сейчас ходит
# class ConditionMotion(Enum):
#     Player = 0
#     Enemy = 1
