from card import Trump, Grant, CardSubType
from collections import deque
from collections.abc import Iterable
from random import shuffle


class Cards:
    """
    カードの配列を扱うクラス
    インデックスが小さい方が先に出す方（山札のトップ側）
    """
    def __init__(self, cards=None):
        if cards is None:
            self.stack = deque()
        elif isinstance(cards, Iterable):
            self.stack = deque(cards)
        else:
            self.stack = deque([cards])

    def push_top(self, card):
        if isinstance(card, Iterable):
            self.stack.extendleft(card)
        else:
            self.stack.appendleft(card)

    def push_bottom(self, card):
        if isinstance(card, Iterable):
            self.stack.extend(card)
        else:
            self.stack.append(card)

    def pop(self):
        return self.stack.popleft()

    def shuffle(self):
        shuffle(self.stack)

    def __getitem__(self, item):
        return self.stack[item]

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        return ', '.join(map(str, self.stack))

    def clear(self):
        return self.stack.clear()


class Hand(Cards):
    """
    手札
    """
    def __init__(self):
        super().__init__()

    def pick(self, index):
        """
        手札を選んで取り出す
        :param index: 取り出す手札の添字
        :return: 取り出したカード
        """
        if isinstance(index, int):
            card = self.stack[index]
            self.stack.remove(card)
            return card
        elif isinstance(index, Iterable):
            cards = [self.stack[i] for i in index]
            for card in cards:
                self.stack.remove(card)
            return cards

    def show(self):
        return ', '.join(['[{}]{}'.format(i, card) for i, card
                          in enumerate(self.stack)])

    def show_not_full_power(self):
        return ', '.join(['[{}]{}'.format(i, card) for i, card
                          in enumerate(self.stack)
                          if not card.is_full_power()])

    def show_full_power(self):
        return ', '.join(['[{}]{}'.format(i, card) for i, card
                          in enumerate(self.stack)
                          if card.is_full_power()])

    def exist_full_power(self):
        return len([1 for card in self.stack if card.is_full_power()]) != 0

    def play(self, index, board, player_type, counter=False):
        self.stack[index].play(board, player_type, counter=counter)


class Trumps:
    """
    決闘中の切り札複数の状態
    """

    def __init__(self, trump_cards):
        self.trumps = [Trump(card) for card in trump_cards]

    def __getitem__(self, item):
        return self.trumps[item]

    def __len__(self):
        return len(self.trumps)

    def __str__(self):
        return ', '.join(map(str, self.trumps))

    def play(self, index, board, player_type, counter=False):
        self.trumps[index].play(board, player_type, counter=counter)

    def show_unused(self):
        return ', '.join(['[1{}]{}'.format(i, trump) for i, trump
                          in enumerate(self.trumps)
                          if not trump.used])

    def show_unused_not_full_power(self):
        return ', '.join(['[1{}]{}'.format(i, trump) for i, trump
                          in enumerate(self.trumps)
                          if not trump.used
                          and not trump.is_full_power()])

    def show_unused_full_power(self):
        return ', '.join(['[1{}]{}'.format(i, trump) for i, trump
                          in enumerate(self.trumps)
                          if not trump.used
                          and trump.is_full_power()])

    def exist_unused_full_power(self):
        return len([1 for trump in self.trumps if trump.is_full_power()
                    and not trump.used]) != 0


class Grants:
    """
    複数の付与札の状態
    TODO: 納を減らす
    """
    def __init__(self):
        self.grants = []

    def __getitem__(self, item):
        return self.grants[item]

    def __len__(self):
        return len(self.grants)

    def __str__(self):
        return str(self.grants)

    def add(self, grant_card, payment):
        self.grants.append(Grant(grant_card, payment))
