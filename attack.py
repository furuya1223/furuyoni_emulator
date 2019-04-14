from area import Area


class Attack:
    def __init__(self, proper_distance, aura_damage, life_damage, uncounterable=False, inevitable=False):
        self.proper_distance = proper_distance  # 適正距離
        self.aura_damage = aura_damage          # オーラダメージ
        self.life_damage = life_damage          # ライフダメージ
        self.uncounterable = uncounterable      # 対応不可
        self.inevitable = inevitable            # 不可避

    def execute(self, board, player_type):
        board.attacks.append(self)
        if not self.uncounterable:
            # 対応
            board.players[player_type.opponent()].counter(board)
            # TODO: 対応後の諸々の判定（間合や決死などの条件の再確認）
            # TODO: 不可避の処理
        if self.aura_damage is None or board.players[player_type.opponent()].aura() < self.aura_damage:
            # オーラダメージが - か、オーラが足りなければ強制的にライフで受ける
            select_aura = False
        elif self.life_damage is None:
            select_aura = True
        else:
            # ダメージの受け方を尋ねる
            print('ダメージ {}/{} をどちらで受けますか？'.format(self.aura_damage, self.life_damage))
            print('[0]: オーラ, [1]: ライフ')
            select_aura = True if input() == '0' else False
        if select_aura:
            # オーラダメージを選択
            # TODO: 「無音壁」展開中かどうか確認し、展開中ならダメージの受け方を尋ねる
            damage = min(board.players[player_type.opponent()].aura(), self.aura_damage)
            Area.move_flowers(board.players[player_type.opponent()].aura, board.dust, damage)
        else:
            # ライフダメージを選択
            damage = min(board.players[player_type.opponent()].life(), self.life_damage)
            Area.move_flowers(board.players[player_type.opponent()].life,
                              board.players[player_type.opponent()].flare, damage)
