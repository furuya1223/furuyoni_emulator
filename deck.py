from card_list import CARD_LIST
from goddess import Goddess


class Deck:
    """
    デッキクラス

    Attributes:
        normal_cards: 通常札
        trump_cards: 切札
        extra_cards: 追加札・毒
    """

    def __init__(self, normal_cards, trump_cards, extra_cards=None):
        # TODO: 追加札はカードから得る（引数で与えない）
        self.normal_cards = normal_cards
        self.trump_cards = trump_cards
        if extra_cards is None:
            self.extra_cards = []
        else:
            self.extra_cards = extra_cards

    def __str__(self):
        return str(self.normal_cards + self.trump_cards)


utsuro_no_kakera_1 = Deck(
    [CARD_LIST[Goddess.UTSURO_HAJIMARI][0][0][i][0] for i in range(7)],
    [CARD_LIST[Goddess.UTSURO_HAJIMARI][0][1][i][0] for i in range(3)]
)
