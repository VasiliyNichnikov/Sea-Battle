from abc import abstractmethod, ABC


class PositionAndSize(ABC):
    @property
    @abstractmethod
    def height(self):
        pass

    @property
    @abstractmethod
    def width(self):
        pass

    @property
    @abstractmethod
    def x(self):
        pass

    @property
    @abstractmethod
    def y(self):
        pass
