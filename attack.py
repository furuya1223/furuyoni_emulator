from area import Area
from copy import copy
from util import generator
from constants import SELECT_AURA, SELECT_LIFE


class Attack:
    def __init__(self, proper_distance, aura_damage, life_damage,
                 uncounterable=False, inevitable=False):
        self.proper_distance = proper_distance  # 適正距離
        self.aura_damage = aura_damage          # オーラダメージ
        self.life_damage = life_damage          # ライフダメージ
        self.uncounterable = uncounterable      # 対応不可
        self.inevitable = inevitable            # 不可避

    def __str__(self):
        string = '{}{}/{}'.format(self.proper_distance, self.aura_damage,
                                  self.life_damage)
        if self.uncounterable:
            string += '(対応不可)'
        if self.inevitable:
            string += '(不可避)'
        return string

    @generator
    def execute(self, board, player_type):
        board.attacks.append(copy(self))
        print(self)
        if not self.uncounterable:
            # 対応
            board.players[player_type.opponent()].counter(board)
            # TODO: 対応後の諸々の判定（間合や決死などの条件の再確認）
            # TODO: 不可避の処理
        attack = board.attacks.pop()
        if attack.aura_damage is None or \
                board.opponent_player().aura() < attack.aura_damage:
            # オーラダメージが - か、オーラが足りなければ強制的にライフで受ける
            select_aura = False
        elif attack.life_damage is None:
            select_aura = True
        else:
            # ダメージの受け方を尋ねる
            while True:
                print('ダメージ {}/{} をどちらで受けますか？'
                      .format(attack.aura_damage, attack.life_damage))
                damage_select = yield '[0]: オーラ, [1]: ライフ'
                if damage_select == SELECT_AURA:
                    select_aura = True
                    break
                elif damage_select == SELECT_LIFE:
                    select_aura = False
                    break
                else:
                    print('入力が不正です！')
        if select_aura:
            # オーラダメージを選択
            # TODO: 「無音壁」展開中かどうか確認し、
            #  展開中ならダメージの受け方を尋ねる
            damage = min(board.opponent_player().aura(), attack.aura_damage)
            Area.move_flowers(board.opponent_player().aura, board.dust, damage)
        else:
            # ライフダメージを選択
            damage = min(board.opponent_player().life(), attack.life_damage)
            Area.move_flowers(board.opponent_player().life,
                              board.opponent_player().flare, damage)
