from enum import Enum, auto
from util import generator


class EffectType(Enum):
    RULE = auto()          # 9-1-1 ルール上効果
    ALWAYS = auto()        # 9-1-2 【常時】効果
    ACTION = auto()        # 9-1-3 行動カード効果
    AFTER_ATTACK = auto()  # 9-1-4 【攻撃後】効果
    EXPAND = auto()        # 9-1-5 【展開時】効果
    UNDERWAY = auto()      # 9-1-6 【展開中】効果
    DISPOSE = auto()       # 9-1-7 【破棄時】効果
    USED = auto()          # 9-1-8 【使用済】効果


class Effect:
    def __init__(self, effect_type, content, summary,
                 arbitrariness=False, condition=None):
        self.effect_type = effect_type
        self.arbitrary = arbitrariness
        self.content = content
        self.summary = summary
        if condition is None:
            self.condition = lambda b, p: True
            pass
        else:
            self.condition = condition

    @generator
    def execute(self, board, player_type):
        print(self.summary)
        if self.condition(board, player_type):
            receive = 1
            if self.arbitrary:
                receive = yield 'この効果を使いますか？'
            if receive == 1:
                self.content(board, player_type)
