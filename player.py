from area import Life, Aura, Flare, Area, AreaType
from cards import Cards, Hand, Trumps, Grants
from deck import Deck
from enum import Enum, auto
from util import generator


class PlayerType(Enum):
    """
    先攻か後攻かを表現する列挙型クラス
    """
    FIRST = auto()   # 先攻
    SECOND = auto()  # 後攻

    def opponent(self):
        """
        Returns:
            PlayerType: 相手のPlayerType
        """
        if self == PlayerType.FIRST:
            return PlayerType.SECOND
        else:
            return PlayerType.FIRST

    def __str__(self):
        if self == PlayerType.FIRST:
            return '先攻'
        else:
            return '後攻'


class Vigor:
    """
    集中力
    """
    def __init__(self, player_type):
        if player_type == PlayerType.FIRST:
            self._value = 0
        else:
            self._value = 1
        self._cowering = False  # 畏縮状態

    def cower(self):
        self._cowering = True

    def recover(self):
        if self._cowering:
            self._cowering = False
        else:
            self._value = min(2, self._value + 1)

    def __iadd__(self, other):
        self._value = min(2, self._value + other)
        return self

    def __isub__(self, other):
        self._value = max(0, self._value - other)
        return self

    def __str__(self):
        if self._cowering:
            return '{}（畏縮）'.format(self._value)
        else:
            return str(self._value)

    def __call__(self, *args, **kwargs):
        return self._value


class Player:
    """
    プレイヤーに紐づく情報を扱うクラス
    ライフ、オーラ、フレア、手札、山札、伏せ札、捨て札、切り札、展開中の付与札、集中力、傘など、
    """
    def __init__(self, player_type: PlayerType, deck: Deck):
        self.life = Life()
        self.aura = Aura()
        self.flare = Flare()
        self.type = player_type
        self.vigor = Vigor(player_type)
        self.hand = Hand()
        self.trumps = Trumps(deck.trump_cards)
        self.stock = Cards(deck.normal_cards)
        self.downed = Cards()
        self.discarded = Cards()
        self.grants = Grants()
        self.extra_cards = Cards(deck.extra_cards)

        # 個別のメガミ関連
        self.umbrella = None
        self.gauge = None
        self.stratagem = None
        self.machine = None

        self.stock.shuffle()

    @generator
    def draw_single(self):
        if len(self.stock) == 0:
            # 焦燥ダメージ
            if self.aura == 0:
                print('焦燥ダメージをライフで受けます')
                select_aura = False
            else:
                # ダメージの受け方を尋ねる
                receive = yield '焦燥ダメージをどちらで受けますか？\n[0]: オーラ, [1]: ライフ'
                select_aura = True if receive == '0' else False
            if select_aura:
                Area.move_flowers(AreaType.AURA, AreaType.DUST, 1)
            else:
                Area.move_flowers(AreaType.LIFE, AreaType.FLARE, 1)
        else:
            self.hand.push_bottom(self.stock.pop())

    def draw(self, number):
        for _ in range(number):
            self.draw_single()

    def down(self, index):
        """
        手札を伏せる
        :param index: 伏せる手札の添字
        """
        self.downed.push_bottom(self.hand.pick(index))

    def discard(self, index):
        """
        手札を捨てる
        :param index: 伏せる手札の添字
        """
        self.discarded.push_bottom(self.hand.pick(index))

    def __str__(self):
        string = '{} オーラ: {}, ライフ: {}, フレア: {}, 集中力: {}, 伏せ札: {}枚, 山札: {}枚, 手札: {}枚, 集中力: {}'\
            .format(self.type,
                    self.aura,
                    self.life,
                    self.flare,
                    self.vigor,
                    len(self.downed),
                    len(self.stock),
                    len(self.hand),
                    self.vigor)
        if len(self.grants) > 0:
            string += '\n' + str(self.grants)
        return string

    def show_hand(self):
        return self.hand.show()

    def show_unused_trumps(self):
        return self.trumps.show_unused()

    def get_counter(self):
        counter_normal_cards = [(i, card) for i, card in enumerate(self.hand) if card.counter]
        counter_trumps = [(i, trump) for i, trump in enumerate(self.trumps) if not trump.used and trump.card.counter]
        return counter_normal_cards, counter_trumps

    @generator
    def counter(self, board):
        # 対応可能か判定
        counter_normal_cards, counter_trumps = self.get_counter()
        if len(counter_normal_cards) == 0 and len(counter_trumps) == 0:
            # 対応不可能
            return
        # 対応カードを表示
        for i, card in counter_normal_cards:
            print('[{}]: {} '.format(i, card), end='')
        print()
        for i, trump in counter_trumps:
            print('[1{}]: {} '.format(i, trump), end='')
        receive = yield '対応する場合はカードの番号を入力してください\n対応しない場合は-1を入力してください'
        receive = int(receive)
        if receive == -1:
            return
        if receive < 10:
            # 通常札
            self.hand.play(receive, board, self.type)
            self.discard(receive)
        else:
            # 切札
            receive -= 10
            self.trumps.play(receive, board, self.type)

    def reconstruction(self, no_damage=False):
        """
        山札の再構成を行う
        # TODO: 設置・虚魚の処理
        """
        self.stock.push_bottom(self.downed.stack)
        self.downed.clear()
        self.stock.push_bottom(self.discarded.stack)
        self.discarded.clear()
        self.stock.shuffle()
        if not no_damage:
            Area.move_flowers(self.life, self.flare, 1)
