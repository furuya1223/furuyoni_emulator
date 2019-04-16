from card import AttackCard, ActionCard, CardSubType
from attack import Attack
from effect import Effect, EffectType
from area import AreaType, Area
from goddess import Goddess
from util import generator


CARD_LIST = {}
"""
CARD_LIST[メガミ番号][メガミ種別][カード種別][番号][追加番号]
メガミ番号は 1～14 （1-indexed）
メガミ種別は 0, 1 （1がアナザー）
カード種別は以下の通り
    0: 通常札
    1: 切札
    2: 毒
追加番号は、通常0。追加札ではEx*の番号がつく
"""
# ウツロのかけら
CARD_LIST[Goddess.UTSURO_HAJIMARI] = [[[], []]]
CARD_LIST[Goddess.UTSURO_HAJIMARI][0][0].append(
    [AttackCard(Goddess.UTSURO_HAJIMARI, '投射', Attack([5, 6, 7, 8, 9], 3, 1),
                image_filename='na_00_hajimari_a_n_1.png')])
CARD_LIST[Goddess.UTSURO_HAJIMARI][0][0].append(
    [AttackCard(Goddess.UTSURO_HAJIMARI, '脇斬り', Attack([2, 3], 2, 2),
                image_filename='na_00_hajimari_a_n_2.png')])
CARD_LIST[Goddess.UTSURO_HAJIMARI][0][0].append(
    [AttackCard(Goddess.UTSURO_HAJIMARI, '牽制', Attack([1, 2, 3], 2, 1),
                image_filename='na_00_hajimari_a_n_3.png')])
CARD_LIST[Goddess.UTSURO_HAJIMARI][0][0].append(
    [AttackCard(Goddess.UTSURO_HAJIMARI, '背中刺し', Attack([1], 3, 2),
                image_filename='na_00_hajimari_a_n_4.png')])
CARD_LIST[Goddess.UTSURO_HAJIMARI][0][0].append(
    [AttackCard(Goddess.UTSURO_HAJIMARI, '二刀一閃', Attack([2, 3], 4, 2),
                image_filename='na_00_hajimari_a_n_5.png',
                sub_type=CardSubType.FULL_POWER)])


def hohou1(board, player_type):
    board.players[player_type].vigor += 1


@generator
def hohou2(board, _):
    receive = yield '[0]: 間合→ダスト, [1]: ダスト→間合'
    if receive == '0':
        Area.move_flowers(board.distance, board.dust, 1)
    else:
        Area.move_flowers(board.dust, board.distance, 1)


CARD_LIST[Goddess.UTSURO_HAJIMARI][0][0].append(
    [ActionCard(Goddess.UTSURO_HAJIMARI, '歩法', effects=[
        Effect(effect_type=EffectType.ACTION,
               content=hohou1,
               summary='集中力を1得る'),
        Effect(effect_type=EffectType.ACTION,
               content=hohou2, summary='間合←→ダスト(1)',
               )
    ],
                image_filename='na_00_hajimari_a_n_6.png')])
CARD_LIST[Goddess.UTSURO_HAJIMARI][0][0].append(
    [ActionCard(Goddess.UTSURO_HAJIMARI, '潜り', effects=[
        Effect(effect_type=EffectType.ACTION,
               content=lambda b, p: Area.move_flowers(b.distance, b.dust, 1),
               summary='間合→ダスト(1)')
    ],
                sub_type=CardSubType.COUNTER,
                image_filename='na_00_hajimari_a_n_7.png')]
)
CARD_LIST[Goddess.UTSURO_HAJIMARI][0][1].append(
    [AttackCard(Goddess.UTSURO_HAJIMARI, '数多ノ刃', Attack([1, 2], 4, 3),
                trump=True, cost=5,
                image_filename='na_00_hajimari_a_s_1.png')])
CARD_LIST[Goddess.UTSURO_HAJIMARI][0][1].append(
    [ActionCard(Goddess.UTSURO_HAJIMARI, '闇凪ノ声', effects=[
        Effect(effect_type=EffectType.ACTION,
               content=lambda b, p: b.players[p].draw(2),
               summary='カードを2枚引く')
    ], trump=True, cost=4, image_filename='na_00_hajimari_a_s_2.png')])


def ku_no_gaitou(board, _):
    attack = board.attacks.pop()
    attack.aura_damage = max(0, attack.aura_damage - 2)
    board.attacks.append(attack)


CARD_LIST[Goddess.UTSURO_HAJIMARI][0][1].append(
    [ActionCard(Goddess.UTSURO_HAJIMARI, '苦ノ外套', effects=[
        Effect(effect_type=EffectType.ACTION, content=ku_no_gaitou,
               summary='対応した攻撃は -2/+0 となる'),
        Effect(effect_type=EffectType.ACTION,
               content=lambda b, p: Area.move_flowers(
                   b.players[p.opponent()].aura, b.dust, 2),
               summary='相オーラ→ダスト(2)')
    ],
                sub_type=CardSubType.COUNTER, trump=True, cost=4,
                image_filename='na_00_hajimari_a_s_3.png')])


# ユリナ
CARD_LIST[Goddess.YURINA] = [[[], []], [[], []]]
# 斬
CARD_LIST[Goddess.YURINA][0][0].append(
    [AttackCard(1, '斬', Attack([3, 4], 3, 1),
     image_filename='na_01_yurina_o_n_1.png')])

# 足捌き
CARD_LIST[Goddess.YURINA][0][0].append([ActionCard(1, '足捌き', effects=[
        Effect(effect_type=EffectType.ACTION,
               condition=lambda b, p: b.distance() >= 4,
               content=lambda b, p: b.move_flower(AreaType.DISTANCE,
                                                  AreaType.DUST, 2, p),
               summary='間合いが4以上なら 間合→ダスト(2)'),
        Effect(effect_type=EffectType.ACTION,
               condition=lambda b, p: b.distance() <= 1,
               content=lambda b, p: Area.move_flowers(b.dust, b.distance, 2),
               summary='間合いが1以下なら ダスト→間合(2)'),
    ], image_filename='na_01_yurina_o_n_5_s2.png')])

# 月影落
CARD_LIST[Goddess.YURINA][0][1].append(
    [AttackCard(1, '月影落',Attack([3, 4], 4, 4), trump=True, cost=7)])
