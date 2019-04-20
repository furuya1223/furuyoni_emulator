from moderator import Moderator
from deck import utsuro_no_kakera_1, honoka_no_kakera_1


def test():
    # ウツロのかけら初期デッキとホノカのかけら初期デッキを設定
    moderator = Moderator(utsuro_no_kakera_1, honoka_no_kakera_1)

    # 決闘開始
    moderator.start_battle()


if __name__ == '__main__':
    test()
