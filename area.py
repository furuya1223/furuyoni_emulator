from abc import ABCMeta, abstractmethod
from enum import Enum, auto

INFINITY = 1000


class AreaType(Enum):
    DISTANCE = auto()
    AURA = auto()
    OPPONENT_AURA = auto()
    LIFE = auto()
    OPPONENT_LIFE = auto()
    FLARE = auto()
    OPPONENT_FLARE = auto()
    DUST = auto()
    OUT_OF_GAME = auto()


class Area(metaclass=ABCMeta):
    """
    桜花結晶が存在しうる領域
    
    Attributes:
        flowers (int): 桜花結晶の数
    """
    def __init__(self, value):
        self.flowers = value

    @abstractmethod
    def removable(self):
        """
        減らせる桜花結晶の数を計算する
        Returns:
            減らせる桜花結晶の数
        """
        pass

    @abstractmethod
    def receivable(self):
        """
        増やせる桜花結晶の数を計算する
        Returns:
            増やせる桜花結晶の数
        """
        pass

    def remove(self, value):
        """
        桜花結晶を減らす
        Args:
            value: 減らす桜花結晶の数
        """
        self.flowers -= value

    def receive(self, value):
        """
        桜花結晶を増やす
        Args:
            value: 増やす桜花結晶の数
        """
        self.flowers += value

    @staticmethod
    def move_flowers(source, destination, value):
        value = min(value, source.removable(), destination.receivable())
        source.remove(value)
        destination.receive(value)

    def __str__(self):
        return str(self.flowers)

    def __call__(self, *args, **kwargs):
        return self.flowers


class Distance(Area):
    def __init__(self):
        super().__init__(3)
        self.increment_token = 0
        self.decrement_token = 0

    def removable(self):
        return self.flowers - self.decrement_token

    def receivable(self):
        return 10 - self.flowers - self.increment_token

    def __call__(self, *args, **kwargs):
        return self.flowers + self.increment_token - self.decrement_token

    def __str__(self):
        string = str(self.__call__())
        if self.increment_token == 0 and self.decrement_token == 0:
            return string
        string += '={}'.format(self.flowers)
        if self.increment_token > 0:
            string += '+{}'.format(self.increment_token)
        if self.decrement_token > 0:
            string += '-{}'.format(self.decrement_token)
        return string


class Aura(Area):
    def __init__(self):
        super().__init__(3)

    def removable(self):
        return self.flowers

    def receivable(self):
        return 5 - self.flowers


class Life(Area):
    def __init__(self):
        super().__init__(10)

    def removable(self):
        return self.flowers

    def receivable(self):
        return INFINITY


class Flare(Area):
    def __init__(self):
        super().__init__(0)

    def removable(self):
        return self.flowers

    def receivable(self):
        return INFINITY


class Dust(Area):
    def __init__(self):
        super().__init__(0)

    def removable(self):
        return self.flowers

    def receivable(self):
        return INFINITY


class OutOfGame(Area):
    def __init__(self):
        super().__init__(INFINITY)

    def removable(self):
        return INFINITY

    def receivable(self):
        return INFINITY
