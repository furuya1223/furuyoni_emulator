from card import AttackCard, ActionCard, CardSubType
from attack import Attack
from effect import Effect, EffectType
from area import AreaType, Area
from goddess import Goddess
from util import generator


class CardList:
    """
    全カードのリスト

    CardList[メガミ番号][メガミ種別][カード種別][番号][追加番号]

    ※仕様はまだ定まっていない

    メガミ番号は :class:`~goddess.Goddess` に従う

    メガミ種別は 0, 1 （1がアナザー）

    カード種別は以下の通り

        - 0: 通常札
        - 1: 切札
        - 2: 毒

    追加番号は、通常0。追加札ではEx*の番号がつく

    Attributes:
        card_list (dict): カードリスト
    """

    def __init__(self):
        """
        全カードを生成しリストに登録
        """
        self.card_list = dict()

        # ウツロのかけら
        self.card_list[Goddess.UTSURO_HAJIMARI] = [[[], []]]
        self.card_list[Goddess.UTSURO_HAJIMARI][0][0].append(
            [AttackCard(Goddess.UTSURO_HAJIMARI, '投射',
                        Attack([5, 6, 7, 8, 9], 3, 1),
                        image_filename='na_00_hajimari_a_n_1.png')])
        self.card_list[Goddess.UTSURO_HAJIMARI][0][0].append(
            [AttackCard(Goddess.UTSURO_HAJIMARI, '脇斬り', Attack([2, 3], 2, 2),
                        image_filename='na_00_hajimari_a_n_2.png')])
        self.card_list[Goddess.UTSURO_HAJIMARI][0][0].append(
            [AttackCard(Goddess.UTSURO_HAJIMARI, '牽制', Attack([1, 2, 3], 2, 1),
                        image_filename='na_00_hajimari_a_n_3.png')])
        self.card_list[Goddess.UTSURO_HAJIMARI][0][0].append(
            [AttackCard(Goddess.UTSURO_HAJIMARI, '背中刺し', Attack([1], 3, 2),
                        image_filename='na_00_hajimari_a_n_4.png')])
        self.card_list[Goddess.UTSURO_HAJIMARI][0][0].append(
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

        self.card_list[Goddess.UTSURO_HAJIMARI][0][0].append(
            [ActionCard(Goddess.UTSURO_HAJIMARI, '歩法', effects=[
                Effect(effect_type=EffectType.ACTION,
                       content=hohou1,
                       summary='集中力を1得る'),
                Effect(effect_type=EffectType.ACTION,
                       content=hohou2, summary='間合←→ダスト(1)',
                       )
            ],
                        image_filename='na_00_hajimari_a_n_6.png')])
        self.card_list[Goddess.UTSURO_HAJIMARI][0][0].append(
            [ActionCard(Goddess.UTSURO_HAJIMARI, '潜り', effects=[
                Effect(effect_type=EffectType.ACTION,
                       content=lambda b, p: Area.move_flowers(b.distance,
                                                              b.dust, 1),
                       summary='間合→ダスト(1)')
            ],
                        sub_type=CardSubType.COUNTER,
                        image_filename='na_00_hajimari_a_n_7.png')]
        )
        self.card_list[Goddess.UTSURO_HAJIMARI][0][1].append(
            [AttackCard(Goddess.UTSURO_HAJIMARI, '数多ノ刃', Attack([1, 2], 4, 3),
                        trump=True, cost=5,
                        image_filename='na_00_hajimari_a_s_1.png')])
        self.card_list[Goddess.UTSURO_HAJIMARI][0][1].append(
            [ActionCard(Goddess.UTSURO_HAJIMARI, '闇凪ノ声', effects=[
                Effect(effect_type=EffectType.ACTION,
                       content=lambda b, p: b.players[p].draw(2),
                       summary='カードを2枚引く')
            ], trump=True, cost=4, image_filename='na_00_hajimari_a_s_2.png')])

        def ku_no_gaitou(board, _):
            attack = board.attacks.pop()
            attack.aura_damage = max(0, attack.aura_damage - 2)
            board.attacks.append(attack)

        self.card_list[Goddess.UTSURO_HAJIMARI][0][1].append(
            [ActionCard(Goddess.UTSURO_HAJIMARI, '苦ノ外套', effects=[
                Effect(effect_type=EffectType.ACTION, content=ku_no_gaitou,
                       summary='対応した攻撃は -2/+0 となる'),
                Effect(effect_type=EffectType.ACTION,
                       content=lambda b, p: Area.move_flowers(
                           b.players[p.opponent()].aura, b.dust, 2),
                       summary='相オーラ→ダスト(2)')
            ],
                        sub_type=CardSubType.COUNTER, trump=True, cost=3,
                        image_filename='na_00_hajimari_a_s_3.png')])

        # ホノカのかけら
        self.card_list[Goddess.HONOKA_HAJIMARI] = [[[], []]]

        self.card_list[Goddess.HONOKA_HAJIMARI][0][0].append(
            [AttackCard(Goddess.HONOKA_HAJIMARI, '花弁刃',
                        Attack([4, 5], None, 1),
                        image_filename='na_00_hajimari_b_n_1.png')])
        self.card_list[Goddess.HONOKA_HAJIMARI][0][0].append(
            [AttackCard(Goddess.HONOKA_HAJIMARI, '桜刀', Attack([3, 4], 3, 1),
                        image_filename='na_00_hajimari_b_n_2.png')])
        self.card_list[Goddess.HONOKA_HAJIMARI][0][0].append(
            [AttackCard(Goddess.HONOKA_HAJIMARI, '瞬霊式', Attack([5], 3, 2,
                                                               uncounterable=True),
                        image_filename='na_00_hajimari_b_n_3.png')])

        def kaeshigiri(board, player_type, counter):
            if counter:
                Area.move_flowers(board.dust, board.players[player_type].aura,
                                  1)

        self.card_list[Goddess.HONOKA_HAJIMARI][0][0].append(
            [AttackCard(Goddess.HONOKA_HAJIMARI, '返し斬り', Attack([3, 4], 2, 1),
                        effects=[
                            Effect(effect_type=EffectType.AFTER_ATTACK,
                                   content=kaeshigiri,
                                   summary='【攻撃後】このカードを対応で'
                                           '使用したならば、ダスト→自オーラ(1)')
                        ],
                        image_filename='na_00_hajimari_b_n_4.png',
                        sub_type=CardSubType.COUNTER)])
        self.card_list[Goddess.HONOKA_HAJIMARI][0][0].append(
            [ActionCard(Goddess.HONOKA_HAJIMARI, '歩法', effects=[
                Effect(effect_type=EffectType.ACTION,
                       content=hohou1,
                       summary='集中力を1得る'),
                Effect(effect_type=EffectType.ACTION,
                       content=hohou2, summary='間合←→ダスト(1)',
                       )
            ],
                        image_filename='na_00_hajimari_b_n_5.png')])
        self.card_list[Goddess.HONOKA_HAJIMARI][0][0].append(
            [ActionCard(Goddess.HONOKA_HAJIMARI, '瞬霊式', effects=[
                Effect(effect_type=EffectType.ACTION,
                       content=lambda b, p:
                       Area.move_flowers(b.players[p.opponent()].aura,
                                         b.players[p].aura, 1),
                       summary='相オーラ→自オーラ(1)')
            ],
                        sub_type=CardSubType.COUNTER,
                        image_filename='na_00_hajimari_b_n_6.png')])
        self.card_list[Goddess.HONOKA_HAJIMARI][0][0].append(
            [ActionCard(Goddess.HONOKA_HAJIMARI, '光輝収束', effects=[
                Effect(effect_type=EffectType.ACTION,
                       content=lambda b, p:
                       Area.move_flowers(b.dust, b.players[p].aura, 2),
                       summary='ダスト→自オーラ(2)'),
                Effect(effect_type=EffectType.ACTION,
                       content=lambda b, p:
                       Area.move_flowers(b.dust, b.players[p].flare, 1),
                       summary='ダスト→自フレア(1)')
            ],
                        sub_type=CardSubType.FULL_POWER,
                        image_filename='na_00_hajimari_b_n_7.png')])
        self.card_list[Goddess.HONOKA_HAJIMARI][0][1].append(
            [AttackCard(Goddess.HONOKA_HAJIMARI, '光満ちる一刀',
                        Attack([3, 4], 4, 3),
                        trump=True, cost=5,
                        image_filename='na_00_hajimari_b_s_1.png')])
        self.card_list[Goddess.HONOKA_HAJIMARI][0][1].append(
            [ActionCard(Goddess.HONOKA_HAJIMARI, '花吹雪の景色', effects=[
                Effect(effect_type=EffectType.ACTION,
                       content=lambda b, p: Area.move_flowers(
                           b[p.opponent()].aura,
                           b.distance, 2),
                       summary='相オーラ→間合(2)')
            ], trump=True, cost=4, image_filename='na_00_hajimari_b_s_2.png')])

        def seirei_tachi_no_kaze(board, _):
            attack = board.attacks.pop()
            if not attack.is_trump:
                attack.canceled = True
            board.attacks.append(attack)

        self.card_list[Goddess.HONOKA_HAJIMARI][0][1].append(
            [ActionCard(Goddess.HONOKA_HAJIMARI, '精霊たちの風', effects=[
                Effect(effect_type=EffectType.ACTION,
                       content=seirei_tachi_no_kaze,
                       summary='対応した切札でない攻撃を打ち消す'),
                Effect(effect_type=EffectType.ACTION,
                       content=lambda b, p: b.players[p].draw(1),
                       summary='カードを1枚引く')
            ],
                        sub_type=CardSubType.COUNTER, trump=True, cost=3,
                        image_filename='na_00_hajimari_b_s_3.png')])

        # ユリナ
        self.card_list[Goddess.YURINA] = [[[], []], [[], []]]
        # 斬
        self.card_list[Goddess.YURINA][0][0].append(
            [AttackCard(1, '斬', Attack([3, 4], 3, 1),
                        image_filename='na_01_yurina_o_n_1.png')])

        # 足捌き
        self.card_list[Goddess.YURINA][0][0].append([ActionCard(1, '足捌き', effects=[
            Effect(effect_type=EffectType.ACTION,
                   condition=lambda b, p: b.distance() >= 4,
                   content=lambda b, p: b.move_flower(AreaType.DISTANCE,
                                                      AreaType.DUST, 2, p),
                   summary='間合いが4以上なら 間合→ダスト(2)'),
            Effect(effect_type=EffectType.ACTION,
                   condition=lambda b, p: b.distance() <= 1,
                   content=lambda b, p: Area.move_flowers(b.dust, b.distance,
                                                          2),
                   summary='間合いが1以下なら ダスト→間合(2)'),
        ], image_filename='na_01_yurina_o_n_5_s2.png')])

        # 月影落
        self.card_list[Goddess.YURINA][0][1].append(
            [AttackCard(1, '月影落', Attack([3, 4], 4, 4), trump=True, cost=7)])

    def __getitem__(self, item):
        """
        指定されたメガミのカードリストを返す

        Args:
            item (Goddess): メガミ

        Returns:
            list: 指定したメガミのカードリスト
        """
        return self.card_list[item]
