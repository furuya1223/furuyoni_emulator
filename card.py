from exception import *
from enum import Enum, auto
from attack import Attack
from effect import EffectType
import os

CARD_IMAGE_DIRECTORY = os.path.join('image', 'cards')


class CardType(Enum):
    ATTACK = auto()     # 攻撃
    ACTION = auto()     # 行動
    GRANT = auto()      # 付与
    UNDEFINED = auto()  # 未確定


class CardSubType(Enum):
    NONE = auto()        # 無し
    COUNTER = auto()     # 対応
    FULL_POWER = auto()  # 全力


class Card:
    def __init__(self, goddess, name, card_type, effects=None,
                 sub_type=CardSubType.NONE, trump=False, cost=None,
                 image_filename=''):
        self.goddess = goddess  # メガミ種別
        self.name = name
        self._card_type = card_type
        self._sub_type = sub_type
        self.trump = trump
        self.cost = cost  # 切札のフレア消費
        if effects is None:
            self.effects = []
        else:
            self.effects = effects
        self.image_url = os.path.join(CARD_IMAGE_DIRECTORY, image_filename)

    def __str__(self):
        if self.is_full_power():
            return self.name + '(全力)'
        else:
            return self.name

    def play(self, board, player, counter=False, **kwargs):
        pass

    def flare_check(self, board, player_type):
        if self.trump:
            cost = self.cost
            # TODO: 灰滅などのコスト変更効果
            # TODO: 責務を移動
            if board.players[player_type].flare.flowers < cost:
                print('フレアが足りません！（{} < {}）'
                      .format(board.players[player_type].flare.flowers, cost))
                raise FlowerLackException

    def is_full_power(self):
        return self._sub_type == CardSubType.FULL_POWER

    def is_counter(self):
        return self._sub_type == CardSubType.COUNTER

    def is_attack(self):
        return self._card_type == CardType.ATTACK

    def is_action(self):
        return self._card_type == CardType.ACTION

    def is_grant(self):
        return self._card_type == CardType.GRANT


class AttackCard(Card):
    def __init__(self, goddess, name, attack,
                 sub_type=CardSubType.NONE, effects=None, trump=False,
                 cost=None, image_filename=''):
        super().__init__(goddess=goddess, name=name, card_type=CardType.ATTACK,
                         effects=effects, sub_type=sub_type, trump=trump, cost=cost,
                         image_filename=image_filename)
        self.base_attack: Attack = attack

    def play(self, board, player, counter=False, **kwargs):
        self.flare_check(board, player)
        attack = self.base_attack
        # TODO: 【常時】効果と現在有効な効果を適用して攻撃を修正する
        # TODO: 適正距離判定はattackのexecuteに行わせる
        if board.distance() not in attack.proper_distance:
            raise DistanceException('現在の間合が適正距離に含まれません！')
        for effect in self.effects:
            if effect.effect_type is EffectType.ALWAYS:
                effect.execute(board, attack)
        if counter:
            # 対応で使用した場合は対応不可が付く
            attack.uncounterable = True
        attack.execute(board, player)
        for effect in self.effects:
            if effect.effect_type is EffectType.AFTER_ATTACK:
                effect.execute(board, attack)


class ActionCard(Card):
    def __init__(self, goddess, name, sub_type=CardSubType.NONE,
                 effects=None, trump=False, cost=None, image_filename=''):
        super().__init__(goddess=goddess, name=name, card_type=CardType.ACTION,
                         effects=effects, sub_type=sub_type, trump=trump,
                         cost=cost, image_filename=image_filename)

    def play(self, board, player, counter=False, **kwargs):
        self.flare_check(board, player)
        for effect in self.effects:
            effect.execute(board, player)


class GrantCard(Card):
    def __init__(self, goddess, name, payment,
                 sub_type=CardSubType.NONE, effects=None, trump=False,
                 cost=None, image_filename=''):
        super().__init__(goddess=goddess, name=name, card_type=CardType.GRANT,
                         effects=effects, sub_type=sub_type, trump=trump,
                         cost=cost, image_filename=image_filename)
        self.payment = payment

    def play(self, board, player, counter=False, **kwargs):
        self.flare_check(board, player)
        # TODO: 展開時効果
        # TODO: 値の有効性判定
        dust = kwargs['dust']
        aura = kwargs['aura']
        if dust == 0 and aura == 0:
            # TODO: 破棄時効果の発動
            pass
        board.dust -= dust
        board.players[player].aura.remove(aura)
        board.players[player].grants.add(self, dust + aura)


class Trump:
    """
    決闘中の切り札1枚の状態
    """
    def __init__(self, trump_card):
        self.card = trump_card
        self.used = False

    def __str__(self):
        if self.used:
            return str(self.card) + '(使用済)'
        else:
            return str(self.card)

    def play(self, board, player_type, counter=False):
        # TODO: usedのときにエラー
        self.card.play(board, player_type, counter=counter)
        self.used = True

    def is_full_power(self):
        return self.card.is_full_power()

    def is_counter(self):
        return self.card.is_counter()


class Grant:
    """
    展開中の付与札の状態
    TODO: 納を減らす、各種効果の発動
    """
    def __init__(self, grand_card, payment):
        self.card = grand_card
        self.flowers = payment

    def __str__(self):
        return '{}({})'.format(self.card, self.flowers)
