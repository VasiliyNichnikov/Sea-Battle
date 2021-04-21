from abc import ABC, abstractmethod


class DrawObject(ABC):
    @abstractmethod
    def draw(self) -> None:
        pass

    # @abstractmethod
    # def update_position(self) -> None:
    #     pass
    #
    # @abstractmethod
    # def update_size(self) -> None:
    #     pass
