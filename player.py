from area import Life, Aura, Flare, Area, AreaType
from cards import Cards, Hand, Trumps, Grants
from deck import Deck
from enum import Enum, auto
from util import generator
from constants import VIGOR_MAX, VIGOR_MIN, VIGOR_DEFAULT_FIRST,\
    VIGOR_DEFAULT_SECOND


class PlayerType(Enum):
    """
    先攻か後攻かを表現する列挙型クラス
    """
    FIRST = auto()   # 先攻
    SECOND = auto()  # 後攻

    def opponent(self):
        """
        相手のタイプを返す
        Returns
        -------
        相手のプレイヤータイプ
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

    Attributes
    ----------
    _value: int
        集中力の値
    _cowering: bool
        畏縮状態かどうか
    """
    def __init__(self, player_type):
        if player_type == PlayerType.FIRST:
            self._value = VIGOR_DEFAULT_FIRST
        else:
            self._value = VIGOR_DEFAULT_SECOND
        self._cowering = False  # 畏縮状態

    def cower(self):
        """
        畏縮させる
        """
        self._cowering = True

    def recover(self):
        """
        集中力を1段階回復する
        """
        if self._cowering:
            self._cowering = False
        else:
            self._value = min(VIGOR_MAX, self._value + 1)

    def __iadd__(self, other):
        """
        集中力を増やす加算代入演算子
        最大値を超えないようにする

        Parameters
        ----------
        other: int
            増やす量

        Returns
        -------
        self: Vigor
            増やした後の自身
        """
        self._value = min(VIGOR_MAX, self._value + other)
        return self

    def __isub__(self, other):
        """
        集中力を減らす減算代入演算子
        最小値を下回らないようにする

        Parameters
        ----------
        other: int
            減らす量

        Returns
        -------
        self: Vigor
            減らした後の自身
        """
        self._value = max(VIGOR_MIN, self._value - other)
        return self

    def __str__(self):
        if self._cowering:
            return '{}（畏縮）'.format(self._value)
        else:
            return str(self._value)

    def __call__(self, *args, **kwargs):
        """
        集中力の値を返す
        Returns
        -------
        集中力の値
        """
        return self._value


class Player:
    """
    プレイヤーに紐づく情報を扱うクラス
    ライフ、オーラ、フレア、手札、山札、伏せ札、捨て札、切り札、
    展開中の付与札、集中力、傘など

    Attributes
    ----------
    life: Life
        ライフ
    aura: Aura
        オーラ
    flare: Flare
        フレア
    type: PlayerType
        プレイヤータイプ（先攻か後攻か）
    vigor: Vigor
        集中力
    hand: Hand
        手札
    trumps: Trumps
        切札
    stock: Cards
        山札
    downed: Cards
        伏せ札
    discarded: Cards
        捨て札
    grants: Grants
        付与札
    extra_cards: Cards
        追加札
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
        """
        山札からカードを1枚ドローする
        山札が無ければ焦燥ダメージを受ける
        """
        if len(self.stock) == 0:
            # 焦燥ダメージ
            if self.aura == 0:
                print('焦燥ダメージをライフで受けます')
                select_aura = False
            else:
                # ダメージの受け方を尋ねる
                receive = yield '焦燥ダメージをどちらで受けますか？\n'\
                                '[0]: オーラ, [1]: ライフ'
                select_aura = True if receive == '0' else False
            if select_aura:
                Area.move_flowers(AreaType.AURA, AreaType.DUST, 1)
            else:
                Area.move_flowers(AreaType.LIFE, AreaType.FLARE, 1)
        else:
            self.hand.push_bottom(self.stock.pop())

    def draw(self, number):
        """
        山札から何枚かカードをドローする

        Parameters
        ----------
        number: int
            ドローする枚数
        """
        for _ in range(number):
            self.draw_single()

    def down(self, index):
        """
        手札を伏せる

        Parameters
        ----------
        index: int
            伏せる手札の添字
        """
        self.downed.push_bottom(self.hand.pick(index))

    def mulligan(self, indices):
        self.stock.push_bottom(self.hand.pick(indices))

    def discard(self, index):
        """
        手札を捨てる

        Parameters
        ----------
        index: int
            捨てる手札の添字
        """
        self.discarded.push_bottom(self.hand.pick(index))

    def __str__(self):
        string = '{} オーラ: {}, ライフ: {}, フレア: {}, 集中力: {}, '\
                 '伏せ札: {}枚, 山札: {}枚, 手札: {}枚, 集中力: {}'\
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

    def show_hand_not_full_power(self):
        return self.hand.show_not_full_power()

    def show_hand_full_power(self):
        return self.hand.show_full_power()

    def show_unused_trumps_not_full_power(self):
        return self.trumps.show_unused_not_full_power()

    def show_unused_trumps_full_power(self):
        return self.trumps.show_unused_full_power()

    def exist_full_power(self):
        return self.hand.exist_full_power() or \
               self.trumps.exist_unused_full_power()

    def get_counter(self):
        counter_normal_cards = \
            [(i, card) for i, card in enumerate(self.hand)
             if card.is_counter()]
        counter_trumps = \
            [(i, trump) for i, trump in enumerate(self.trumps)
             if not trump.used and trump.card.is_counter()]
        return counter_normal_cards, counter_trumps

    @generator
    def counter(self, board):
        """
        対応を行うかどうかを尋ね、適切に処理する

        Parameters
        ----------
        board: Board
            現在の局面
        """
        # 対応可能か判定
        counter_normal_cards, counter_trumps = self.get_counter()
        if len(counter_normal_cards) == 0 and len(counter_trumps) == 0:
            # 対応不可能
            return
        # 対応カードを表示
        # TODO 表示をもっとコンパクトに記述する
        print(', '.join(['[{}]: {}'.format(i, card) for i, card
                         in counter_normal_cards]))
        print(', '.join(['[1{}]: {}'.format(i, trump) for i, trump
                         in counter_trumps]))

        receive = yield '対応する場合はカードの番号を入力してください\n'\
                        '対応しない場合は-1を入力してください'
        receive = int(receive)
        if receive == -1:
            return
        if receive < 10:
            # 通常札
            self.hand.play(receive, board, self.type, counter=True)
            self.discard(receive)
        else:
            # 切札
            receive -= 10
            self.trumps.play(receive, board, self.type, counter=True)

    def reconstruction(self, no_damage=False):
        """
        山札の再構成を行う
        TODO: 設置・虚魚の処理

        Parameters
        ----------
        no_damage: bool, default False
            ダメージを受けない場合にTrue
        """
        self.stock.push_bottom(self.downed.stack)
        self.downed.clear()
        self.stock.push_bottom(self.discarded.stack)
        self.discarded.clear()
        self.stock.shuffle()
        if not no_damage:
            Area.move_flowers(self.life, self.flare, 1)
