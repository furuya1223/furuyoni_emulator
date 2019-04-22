"""
桜花結晶が存在する領域を扱うモジュール
"""
from abc import ABCMeta, abstractmethod
from constants import DISTANCE_DEFAULT, AURA_DEFAULT, LIFE_DEFAULT, \
    FLARE_DEFAULT, DUST_DEFAULT, INFINITY


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
        """
        桜花結晶を可能な限り移動する関数

        Args:
            source (Area): 移動元エリア
            destination (Area): 移動先エリア
            value (int): 移動する数
        """
        value = min(value, source.removable(), destination.receivable())
        source.remove(value)
        destination.receive(value)

    def __str__(self):
        return str(self.flowers)

    def __call__(self, *args, **kwargs):
        return self.flowers


class Distance(Area):
    """
    間合エリア

    Attributes:
        increment_token (int): 間合+1トークンの数
        decrement_token (int): 間合-1トークンの数
    """
    def __init__(self):
        super().__init__(DISTANCE_DEFAULT)
        self.increment_token = 0
        self.decrement_token = 0

    def removable(self):
        """
        減らせる桜花結晶の数を計算する

        Returns:
            減らせる桜花結晶の数
        """
        return self.flowers - self.decrement_token

    def receivable(self):
        """
        増やせる桜花結晶の数を計算する

        Returns:
            増やせる桜花結晶の数
        """
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
    """
    オーラ
    """
    def __init__(self):
        super().__init__(AURA_DEFAULT)

    def removable(self):
        """
        減らせる桜花結晶の数を計算する

        Returns:
            減らせる桜花結晶の数
        """
        return self.flowers

    def receivable(self):
        """
        増やせる桜花結晶の数を計算する

        Returns:
            増やせる桜花結晶の数
        """
        return 5 - self.flowers


class Life(Area):
    """
    ライフ
    """
    def __init__(self):
        super().__init__(LIFE_DEFAULT)

    def removable(self):
        """
        減らせる桜花結晶の数を計算する

        Returns:
            減らせる桜花結晶の数
        """
        return self.flowers

    def receivable(self):
        """
        増やせる桜花結晶の数を計算する

        Returns:
            増やせる桜花結晶の数
        """
        return INFINITY


class Flare(Area):
    """
    フレア
    """
    def __init__(self):
        super().__init__(FLARE_DEFAULT)

    def removable(self):
        """
        減らせる桜花結晶の数を計算する

        Returns:
            減らせる桜花結晶の数
        """
        return self.flowers

    def receivable(self):
        """
        増やせる桜花結晶の数を計算する

        Returns:
            増やせる桜花結晶の数
        """
        return INFINITY


class Dust(Area):
    """
    ダスト
    """
    def __init__(self):
        super().__init__(DUST_DEFAULT)

    def removable(self):
        """
        減らせる桜花結晶の数を計算する

        Returns:
            減らせる桜花結晶の数
        """
        return self.flowers

    def receivable(self):
        """
        増やせる桜花結晶の数を計算する

        Returns:
            増やせる桜花結晶の数
        """
        return INFINITY


class OutOfGame(Area):
    """
    ゲーム外
    """
    def __init__(self):
        super().__init__(INFINITY)

    def removable(self):
        """
        減らせる桜花結晶の数を計算する

        Returns:
            減らせる桜花結晶の数
        """
        return INFINITY

    def receivable(self):
        """
        増やせる桜花結晶の数を計算する
        
        Returns:
            増やせる桜花結晶の数
        """
        return INFINITY
