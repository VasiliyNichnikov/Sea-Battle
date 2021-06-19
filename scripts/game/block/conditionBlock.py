from scripts.game2.block.condition import EnumBlock


class ConditionBlock:
    __condition = None

    def __init__(self):
        self.change_to_empty()

    @property
    def condition(self):
        return self.__condition

    def change_to_lock(self) -> None:
        self.__condition = EnumBlock.Lock

    def change_to_empty(self) -> None:
        self.__condition = EnumBlock.Empty

    def change_to_hit(self) -> None:
        self.__condition = EnumBlock.Hit

    def change_to_miss(self) -> None:
        self.__condition = EnumBlock.Miss

    def change_to_selected(self) -> None:
        self.__condition = EnumBlock.Selected
