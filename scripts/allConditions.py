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
    DrawMap = 0
    CheckInputMouse = 1
    DestroyBlock = 2
    HitBlock = 3
    MissBlock = 4


# Состояние корабля
class ConditionShip(Enum):
    Afloat = 0
    Destroyed = 1


# Ось на которой расположен корабль
class ConditionAxisShip(Enum):
    Horizontal = 0
    Vertical = 1


# Состояние блока



# Состояние кнопок в меню
class ConditionButton(Enum):
    NONE = 0
    Play = 1
    Exit = 2
