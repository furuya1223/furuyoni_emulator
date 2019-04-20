from card_list import CardList
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


card_list = CardList()

# ウツロのかけら初期デッキ
utsuro_no_kakera_1 = Deck(
    [card_list[Goddess.UTSURO_HAJIMARI][0][0][i][0] for i in range(7)],
    [card_list[Goddess.UTSURO_HAJIMARI][0][1][i][0] for i in range(3)]
)

# ホノカのかけら初期デッキ
honoka_no_kakera_1 = Deck(
    [card_list[Goddess.HONOKA_HAJIMARI][0][0][i][0] for i in range(7)],
    [card_list[Goddess.HONOKA_HAJIMARI][0][1][i][0] for i in range(3)]
)
