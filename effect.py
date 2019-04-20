"""
効果に関連するモジュール
"""
from enum import Enum, auto
from util import generator
from inspect import signature, isgeneratorfunction
from constants import YES, NO


class EffectType(Enum):
    """
    効果の種別
    """
    RULE = auto()          # 9-1-1 ルール上効果
    ALWAYS = auto()        # 9-1-2 【常時】効果
    ACTION = auto()        # 9-1-3 行動カード効果
    AFTER_ATTACK = auto()  # 9-1-4 【攻撃後】効果
    EXPAND = auto()        # 9-1-5 【展開時】効果
    UNDERWAY = auto()      # 9-1-6 【展開中】効果
    DISPOSE = auto()       # 9-1-7 【破棄時】効果
    USED = auto()          # 9-1-8 【使用済】効果


class Effect:
    """
    効果

    Attributes:
        effect_type (EffectType): 効果の種別
        arbitrariness (bool): 任意性．使わないことが可能なら ``True``
        content (func): 効果の本体．ジェネレータ関数の場合もある
        summary (str): 効果の概要を表す文字列
    """
    def __init__(self, effect_type, content, summary,
                 arbitrariness=False, condition=None):
        self.effect_type = effect_type
        self.arbitrariness = arbitrariness
        self.content = content
        self.summary = summary
        if condition is None:
            self.condition = lambda b, p: True
            pass
        else:
            self.condition = condition

    @generator
    def execute(self, board, player_type, counter=False):
        """
        効果を実行する

        Args:
            board (Board): 現在の局面
            player_type (PlayerType): プレイヤータイプ（先攻か後攻か）
            counter (bool): 対応での使用なら ``True`` ．デフォルトでは ``False``
        """
        print(self.summary)
        if self.condition(board, player_type):
            receive = YES
            if self.arbitrariness:
                receive = yield 'この効果を使いますか？[{}/{}]'.format(YES, NO)
            if receive == NO:
                raise StopIteration
        sig = signature(self.content)
        arguments = [board, player_type]
        if 'counter' in sig.parameters:
            arguments.append(counter)
        if isgeneratorfunction(self.execute):
            yield from self.content(*arguments)
        else:
            self.content(*arguments)
